# https://www.cnblogs.com/sddai/p/14406799.html

import sys; sys.path.append(".")

import chromadb
from typing import List
from chromadb.utils import embedding_functions
from pprint import pprint
from datetime import datetime

from utils.vector_db import DBIndex, DBResult, to_messages, split_name
from utils.prompt import Assistant
from utils.config import Config
# import utils.time as timeUtils
from utils.time import get_now_timestamp, MINUTE

embedding_model = "distiluse-base-multilingual-cased-v1"
database_path = Config.DatabasePath
    
class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=database_path)
        self.embedding_function = embedding_functions \
            .SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        
    def init(self, index: DBIndex, is_strict: bool=True):
        """initialize database using DBIndex
        Args:
            index (DBIndex): the only identifier about database
            is_strict (bool): it will raise error when meet duplication 
                if it's strict

        Raises:
            ValueError: botRole has existed
        """
        try:
            self.client.create_collection(name=index.to_name())
        except:
            if is_strict:
                raise ValueError('botRole has existed')

    def __get_collection(self, index: DBIndex):
        try:   
            database_name = index.to_name()
            return self.client.get_collection(
                database_name, 
                embedding_function=self.embedding_function
            ) 
        except ValueError:
            raise FileNotFoundError(f"database '{database_name}' not found")
        
    def get_database_list(self):
        names = [ collection.name for collection in self.client.list_collections()]
        
        result = {}
        for name in names:
            (key, role) = split_name(name)
            try:
                result[key].append(role)
            except KeyError:
                result[key] = [role]

        return result
    
    '''
    append message to database,
    if the times is None, we'll set the time to now
    '''
    def append_messages(
        self, index: DBIndex,
        contents: List[str], 
        roles: List[str], 
        times: List[datetime]=None
    ):
        if times == None:
            times = [datetime.now()] * 3

        if len(contents) != len(roles) or len(contents) != len(times):
            raise ValueError('the length of elements is not same')

        collection = self.__get_collection(index)
        start_id = collection.count()
        
        # generate id for those content
        ids = [start_id + i for i in range(0, len(contents)) ]        

        self.__get_collection(index) \
            .add(
                # Notice: use leading zeros to order the message
                ids=["%5d"%id for id in ids], 
                documents=contents, 
                metadatas=[{
                    "id": id,
                    "role": role,
                    # Notice: chroma can't receive datetime, so we should use timestamp
                    "time": time.timestamp()
                } for (role, id, time) in zip(roles, ids, times)]
            )
        
    def clear_messages(self, index: DBIndex):
        name = index.to_name()

        self.client.delete_collection(name)
        self.client.create_collection(name)

    def get_messages(self, index: DBIndex, need_id: bool=False, need_time: bool=False):
        result = self.__get_collection(index).get()
        return to_messages(result, need_id=need_id, need_time=need_time)
    
    def get_nearest_messages(self, index: DBIndex, 
        number: int=10, offset: int=0, n: int=10,
        need_id: bool=False, need_time: bool=False
    ) -> DBResult:
        """return the message in n minutes

        Args:
            index (DBIndex): database index
            number (int, optional): maximum number of messages to return . Defaults to 10.
            offset (int, optional): the offset. Defaults to 0.
            n (int, optional): unit of n is minutes. Defaults to 10.

        Returns:
            DBResult: nearest messages
        """

        collection = self.__get_collection(index)
        count = collection.count()

        begin_id = count - offset - number
        end_id = count - offset
        
        condition = [
            { "id": { "$gte": begin_id }},
            { "id": { "$lt": end_id }}
        ]
        
        if n != -1:
            condition.append({'time': {"$gte": get_now_timestamp() - n * MINUTE}})

        result = collection.get(where={"$and": condition})
        messages = to_messages(result, need_id=need_id, need_time=need_time)
        # Notice: update the begin_id
        begin_id = end_id - len(messages)

        return DBResult(messages, begin_id, end_id)

    
    def query(self, index: DBIndex, message: str):
        collection = self.__get_collection(index)
        result = collection.query(query_texts=message, n_results=1)

        messages = to_messages(result, is_multiple=True)
        print(messages)

        return messages

    def query_similar_context(self, index: DBIndex, message: str, window_size: int=3, threshold: float=1) -> DBResult:
        """it will not only return the related message, but also the context

        Args:
            index (DBIndex): the index of the database
            message (str): the identifier to the database.
            window_size (int, optional): the maximum number of message pairs will return. 
                Defaults to 3.

        Returns:
            DBResult
        """

        collection = self.__get_collection(index)
        
        # 1. query the most similar message about this message
        result = collection.query(query_texts=message, n_results=1)

        if len(result["distances"][0]) == 0:
            return DBResult([], -1, -1)
        
        # print("threshold: ", result["distances"][0])
        # print("document: ", result["documents"][0])
        if result["distances"][0][0] > threshold:
            return DBResult([], -1, -1)
        
        similar_messages = to_messages(result, is_multiple=True, need_id=True)
        message = similar_messages[0]

        # 2. get the query message instead of answer message from assistant
        id = message['id']
        id = id - 1 if message['role'] == Assistant else id

        # 3. get the begin and end index of context
        ahead_size = int(window_size / 2)
        begin_id = max(id - ahead_size * 2, 0)
        end_id = id + (window_size - ahead_size) * 2
        
        # 4. using bool condition to get the message in this context
        context_result = collection.get(where={
            "$and": [
                {"id": {"$gte": begin_id}},
                {"id": {"$lt": end_id}}
            ]
        })

        return DBResult(to_messages(context_result), begin_id, end_id)

    def debug(self):
        print("debug: ", self.client.list_collections())

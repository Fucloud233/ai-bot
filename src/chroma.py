# https://www.cnblogs.com/sddai/p/14406799.html

import sys; sys.path.append(".")

import chromadb
from typing import List
from chromadb.utils import embedding_functions
from pprint import pprint
from datetime import datetime

from utils.vector_db import to_messages
from utils.prompt import Assistant
from utils.config import Config

embedding_model = "distiluse-base-multilingual-cased-v1"
database_path = Config.DatabasePath

def merge_name(phone: str, bot_role):
    return phone + '-' + bot_role

def unwrap_name(info):
    try:
        return info["phone"] + '-' + info["botRole"]
    except KeyError:
        raise KeyError("key info not found")
    
class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=database_path)
        self.embedding_function = embedding_functions \
            .SentenceTransformerEmbeddingFunction(model_name=embedding_model)
        
    def init(self, info):
        try:
            self.client.create_collection(name=unwrap_name(info))
        except:
            raise ValueError('botRole has existed')

    def __get_collection(self, info):
        try:   
            database_name = unwrap_name(info)
            return self.client.get_collection(
                database_name, 
                embedding_function=self.embedding_function
            ) 
        except ValueError:
            raise FileNotFoundError(f"database '{database_name}' not found")

    '''
    append message to database,
    if the times is None, we'll set the time to now
    '''
    def append_messages(
        self, info, 
        contents: List[str], 
        roles: List[str], 
        times: List[datetime]=None
    ):
        if times == None:
            times = [datetime.now()] * 3

        if len(contents) != len(roles) or len(contents) != len(times):
            raise ValueError('the length of elements is not same')

        collection = self.__get_collection(info)
        start_id = collection.count()
        
        # generate id for those content
        ids = [start_id + i for i in range(0, len(contents)) ]        

        self.__get_collection(info) \
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
        
    def clear_messages(self, info):
        name = unwrap_name(info)

        self.client.delete_collection(name)
        self.client.create_collection(name)

    def get_messages(self, info, need_id: bool=False, need_time: bool=False):
        result = self.__get_collection(info).get()
        return to_messages(result, need_id=need_id, need_time=need_time)
    
    # TODO: check duplicated message between query messages and history messages
    def query(self, info, message: str):
        collection = self.__get_collection(info)
        result = collection.query(query_texts=message, n_results=1)

        messages = to_messages(result, is_multiple=True)
        print(messages)

        return messages

    def query_with_context(self, info, message: str, window_size: int=3):
        """it will not only return the related message, but also the context

        Args:
            info (_type_): None
            message (str): the identifier to the database.
            window_size (int, optional): the maximum number of message pairs will return. 
                Defaults to 3.

        Returns:
            List[str]: messages
        """

        collection = self.__get_collection(info)
        
        # 1. query the most similar message about this message
        result = collection.query(query_texts=message, n_results=1)
        similar_messages = to_messages(result, is_multiple=True, need_id=True)
        if len(similar_messages) == 0:
            return []
        message = similar_messages[0]

        # 2. get the query message instead of answer message from assistant
        id = message['id']
        id = id - 1 if message['role'] == Assistant else id

        # 3. get the begin and end index of context
        ahead_size = int(window_size / 2)
        begin_id = id - ahead_size * 2
        end_id = id + (window_size - ahead_size) * 2
        
        # 4. using bool condition to get the message in this context
        context_result = collection.get(where={
            "id": {
                "$gte": begin_id
            },
            "id": {
                "$lt": end_id
            }
        })

        return to_messages(context_result)

    def debug(self):
        print("debug: ", self.client.list_collections())

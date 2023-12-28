# https://www.cnblogs.com/sddai/p/14406799.html

import sys; sys.path.append(".")

import chromadb
from typing import List
from chromadb.utils import embedding_functions
from pprint import pprint

from utils.vector_db import to_messages
from utils.prompt import Assistant

embedding_model = "distiluse-base-multilingual-cased-v1"

def merge_name(phone: str, bot_role):
    return phone + '-' + bot_role

def unwrap_name(info):
    try:
        return info["phone"] + '-' + info["botRole"]
    except KeyError:
        raise KeyError("key info not found")
    
class VectorDB:
    def __init__(self, path: str='chroma/'):
        self.client = chromadb.PersistentClient(path=path)
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

    def append_messages(self, info, contents: List[str], roles: List[str]):
        if len(contents) != len(roles):
            raise ValueError('the length of contents is not equal with the roles')

        collection = self.__get_collection(info)
        start_id = collection.count()
        
        # generate id for those content
        ids = [start_id + i for i in range(0, len(contents)) ]        

        print(roles, ids)
        self.__get_collection(info) \
            .add(
                ids=[str(id) for id in ids], 
                documents=contents, 
                metadatas=[{
                    "id": id,
                    "role": role,
                } for role, id in zip(roles, ids)]
            )
    
    def clear_messages(self, info):
        name = unwrap_name(info)

        self.client.delete_collection(name)
        self.client.create_collection(name)

    def get_messages(self, info):
        result = self.__get_collection(info).get()
        return to_messages(result, need_id=True)
    
    # TODO: check duplicated message between query messages and history messages
    def query(self, info, message: str):
        collection = self.__get_collection(info)
        result = collection.query(query_texts=message, n_results=1)

        messages = to_messages(result, is_multiple=True)
        print(messages)

        return messages
    
    '''
    it will not only return the related message,
    but also the context

    Parameters:
        info: the identifier to the database
        windows_size: the maximum number of message pairs will return
    '''
    def query_with_context(self, info, message: str, window_size: int=3):
        collection = self.__get_collection(info)
        
        # 1. query the most similar message about this message
        result = collection.query(query_texts=message, n_results=1)
        message = to_messages(result, is_multiple=True, need_id=True)[0]

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

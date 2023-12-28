import sys; sys.path.append(".")

import chromadb
from typing import List
from chromadb.utils import embedding_functions

from utils.error import UserNotFound, UserExist
from utils.vector_db import to_messages


def merge_name(phone: str, bot_role):
    return phone + '-' + bot_role

def unwrap_name(info):
    try:
        return info["phone"] + '-' + info["botRole"]
    except:
        raise KeyError("key info not found")
    
class VectorDB:
    def __init__(self, path: str='chroma/'):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_function = embedding_functions \
            .SentenceTransformerEmbeddingFunction(model_name='gtr-t5-base')
        
    def init(self, info):
        try:
            self.client.create_collection(name=unwrap_name(info))
        except:
            raise ValueError('botRole has existed')

    def __get_collection(self, info):
        try:
            return self.client.get_collection(
                unwrap_name(info), 
                embedding_function=self.embedding_function
            ) 
        except ValueError:
            raise UserNotFound

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

    def debug(self):
        print("debug: ", self.client.list_collections())

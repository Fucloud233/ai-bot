import sys; sys.path.append(".")

import chromadb
from typing import List
from chromadb.utils import embedding_functions

from utils.error import UserNotFound, UserExist
 
 
    
class VectorDB:
    def __init__(self, path: str='chroma/'):
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_function = embedding_functions \
            .SentenceTransformerEmbeddingFunction(model_name='gtr-t5-base')

    def init(self, name: str):
        try:
            self.client.create_collection(name=name)
        except:
            raise UserExist


    def __get_collection(self, phone: str):
        try:
            return self.client.get_collection(phone, embedding_function=self.embedding_function) 
        except ValueError:
            raise UserNotFound

    def append_messages(self, phone: str, contents: List[str], roles: List[str]):
        if len(contents) != len(roles):
            raise ValueError('the length of contents is not equal with the roles')

        collection = self.__get_collection(phone)
        start_id = collection.count()
        
        # generate id for those content
        ids = [start_id + i for i in range(0, len(contents)) ]        

        print(roles, ids)
        self.__get_collection(phone) \
            .add(
                ids=[str(id) for id in ids], 
                documents=contents, 
                metadatas=[{
                    "id": id,
                    "role": role,
                } for role, id in zip(roles, ids)]
            )
    
    def clear_messages(self, phone: str):
        self.client.delete_collection(phone)
        self.client.create_collection(phone)

    def get_messages(self, phone: str):
        return self.__get_collection(phone).get()
    
    def debug(self):
        print("debug: ", self.client.list_collections())

from datetime import datetime
from typing import List
from chromadb import QueryResult

PHONE = 'phone'
BOT_ROLE = 'botRole'

class DBIndex:
    def __init__(self, phone: str, bot_role: str):
        self.__phone = phone
        self.__bot_role = bot_role

    @property
    def phone(self) -> str:
        return self.__phone
    
    @property
    def bot_role(self) -> str:
        return self.__bot_role
    
    def to_name(self) -> str:
        return self.phone + '-' + self.bot_role
    
def split_name(name: str) -> (str, str):
    parts = name.split('-')
    return (parts[0], parts[1])
    
class DBResult:
    def __init__(self, messages: List[str], begin_id: int, end_id: int):
        self.__messages = messages
        self.__begin_id = begin_id
        self.__end_id = end_id

    def format(self):
        contents = [message['content'] for message in self.messages]
        roles = [message['role'] for message in self.messages]
        return contents, roles
    
    @property
    def messages(self):
        return self.__messages

    @property
    def begin(self):
        return self.__begin_id

    @property
    def end(self):
        return self.__end_id
    
    @property
    def size(self):
        return self.__end_id - self.__begin_id

def format_messages(messages):
    contents = [message['content'] for message in messages]
    roles = [message['role'] for message in messages]

    return contents, roles

# def to_messages(documents, metadatas):
#     messages = []
#     for (document, metadata) in zip(documents, metadatas):
#         messages.append({
#             "role": metadata['role'],
#             "content": document,
#             "id": metadata['id'],
#         })

#     return messages

def unwrap_array(array, is_multiple: bool):
    return array[0] if is_multiple else array

def to_messages(
    result: QueryResult, 
    is_multiple: bool=False, 
    need_id: bool=False,
    need_time: bool=False
):
    """convert QueryResult to Message {role, content, time}

    Args:
        result (QueryResult): the QueryResult
        is_multiple (bool, optional): if there are multiple documents in result, 
            it will select the first. Defaults to False.
        need_id (bool, optional): whether return id. Defaults to False.
        need_time (bool, optional): whether return time. Defaults to False.

    Returns:
        List[str]: Messages
    """
    documents = unwrap_array(result['documents'], is_multiple)
    metadatas = unwrap_array(result['metadatas'], is_multiple)

    messages = []
    for (document, metadata) in zip(documents, metadatas):
        messages.append({
            "role": metadata['role'],
            "content": document,
            # "id": metadata['id'],
        })

    if need_id:
        for (message, metadata) in zip(messages, metadatas):
            message['id'] = metadata['id']
    if need_time:
        for (message, metadata) in zip(messages, metadatas):
            try:
                # Notice: convert timestamp to string
                message['time'] = datetime.strftime(
                    datetime.fromtimestamp(metadata['time']), 
                    '%Y-%m-%d %H:%M:%S'
                )
            except KeyError:
                pass

    return messages
    

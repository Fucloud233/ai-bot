from chromadb import QueryResult

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

def to_messages(result: QueryResult, is_multiple: bool=False, need_id: bool=False):
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

    return messages
    

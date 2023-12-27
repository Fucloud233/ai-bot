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

def to_messages(result: QueryResult, need_id: bool=False):
    messages = []
    for (document, metadata) in zip(result['documents'], result['metadatas']):
        messages.append({
            "role": metadata['role'],
            "content": document,
            # "id": metadata['id'],
        })

    if need_id:
        for (message, id) in zip(messages, result['ids']):
            message['id'] = id

    return messages
    

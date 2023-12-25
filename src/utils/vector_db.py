def format_messages(messages):
    contents = [message['content'] for message in messages]
    roles = [message['role'] for message in messages]

    return contents, roles

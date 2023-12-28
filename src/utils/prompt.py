
# role
User = 'user'
Assistant = 'assistant'

def wrap_prompt(prompt, answer: str="好的，我知道了。"):
    # messages must have an odd number of elements
    return [{
        "role": "user",
        "content": prompt
    }, {
        "role": "assistant",
        "content": answer
    }]


def wrap_user_prompt(prompt):
    return {
        "role": "user",
        "content": prompt
    }
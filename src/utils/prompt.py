from enum import Enum

# role
User = 'user'
Assistant = 'assistant'

class BotRole(Enum):
    Parent = 'parent'
    Bestie = 'bestie'
    Friend = 'friend'
    Doctor = 'doctor'

    def new(role_name): 
        return BotRole(role_name)
    
    def get_label(self) -> str:
        match self:
            case BotRole.Parent: return "父母"
            case BotRole.Bestie: return "闺蜜"
            case BotRole.Friend: return "朋友"
            case BotRole.Doctor: return "心理医生"

def wrap_prompt(prompt, answer: str=""):
    messages = [{
        "role": "user",
        "content": prompt
    }]

    # messages must have an odd number of elements
    if answer != "":
        messages.append({
            "role": "user",
            "content": prompt
        })

    return messages


def wrap_user_prompt(prompt):
    return {
        "role": "user",
        "content": prompt
    }
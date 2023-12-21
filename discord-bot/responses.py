import random

HELLO = 'hello'
ROLL = 'roll'
HELP = 'help'


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == HELLO:
        return 'Well hello!'
    
    if p_message == ROLL:
        return str(random.randint(1,6))
    
    if p_message == HELP:
        return 'Stop it. Get some help.'

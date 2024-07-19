
#Utility Helper Functions that supports main Menthods and Functions

# Author: Krupananda Reddy


import random
import string

def generate_random_id(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

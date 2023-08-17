# Python
import random
import string


def generate_code(len: int = 6):
    code_data = string.ascii_letters + string.digits
    code = [random.choice(code_data) for _ in range(len)]
    return "".join(code)
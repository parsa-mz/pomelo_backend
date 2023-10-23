import hashlib
import random
from string import ascii_uppercase, digits


# create a random n digit uid str
def make_uid(n):
    return ''.join(random.choice(ascii_uppercase + digits) for _ in range(n))


# hash password
def hash_(password):
    return hashlib.sha256(password.encode()).hexdigest()


# print red
def p_r(text: str):
    return "\033[1;31m" + text + "\033[0m"


# print green
def p_g(text: str):
    return "\033[1;32m" + text + "\033[0m"


# print yellow
def p_y(text: str):
    return "\033[1;33m" + text + "\033[0m"


# print blue
def p_b(text: str):
    return "\033[1;34m" + text + "\033[0m"


# print purple
def p_p(text: str):
    return "\033[1;35m" + text + "\033[0m"


# print cyan
def p_c(text: str):
    return "\033[1;36m" + text + "\033[0m"


# print white
def p_w(text: str):
    return "\033[1;37m" + text + "\033[0m"
import re


def check_email_address(email: str) -> bool:

    '''Checking if email like qwerty76@gmail.com'''

    return bool(re.findall(r"([A-zА-я0-9]+?[@][A-zА-я]+[.][A-zА-я]+)", string=email))
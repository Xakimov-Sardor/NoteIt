def get_time():
    from datetime import datetime
    return datetime.now()


def email_format(email):
    from re import match
    temp = '[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'
    return match(temp, email)

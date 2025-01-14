

def cookie_parser(cookie_str):
    cookie_dict = {}
    for cookie in cookie_str.split(';'):
        key = cookie.split('=')[0]
        value = '='.join(cookie.split('=')[1:])
        cookie_dict[key] = value
    return cookie_dict
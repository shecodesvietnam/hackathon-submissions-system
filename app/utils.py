import random
import string
import re


def generate_random_password(length=12):
    # Get random password of given length with letters, digits, and symbols
    # characters = string.ascii_letters + string.digits + string.punctuation
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f'password = {password}')
    return password


def generate_username(team_name):
    username = team_name.strip().lower()
    reg_username = re.split(' +', username)
    res = []
    for word in reg_username:
        for char in word:
            res.append(get_ascii_character(char))
        if word == reg_username[-1]:
            continue
        else:
            res.append('-')
    print(res)
    return ''.join(res)


def get_ascii_character(char):
    char_e = ['e', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ']
    char_y = ['y', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ']
    char_u = ['u', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự']
    char_i = ['i', 'í', 'ì', 'ỉ', 'ĩ', 'ị']
    char_o = ['o', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ']
    char_a = ['a', 'á', 'à', 'ả', 'ã', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ']
    char_d = ['d', 'đ']

    if char in char_e:
        char = 'e'
    elif char in char_a:
        char = 'a'
    elif char in char_y:
        char = 'y'
    elif char in char_i:
        char = 'i'
    elif char in char_u:
        char = 'u'
    elif char in char_o:
        char = 'o'
    elif char in char_d:
        char = 'd'
    
    return char


def is_valid_url(url):
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    # Compile the ReGex
    compiler = re.compile(regex)
 
    # Return False if url is empty
    if url == None:
        return False
 
    # Return if the string matched the ReGex
    if re.search(compiler, url):
        return True
    return False
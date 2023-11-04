def is_str(token):
    return token.isalpha()


def is_num(token):
    return token.isdigit()


def is_col(c):
    return True if c == ':' else False


def is_symbol(token):
    symbol = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';']
    return True if token in symbol else False


def read_file(file_name):
    with open(file_name, 'r') as f:
        input_text = f.read()
        input_text = input_text.replace('\n', ' ')
        input_text += ' '
        return input_text

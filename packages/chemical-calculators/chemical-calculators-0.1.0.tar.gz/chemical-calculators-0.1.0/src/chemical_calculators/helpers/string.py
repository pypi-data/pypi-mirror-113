'''
Some helpers for main scripts.
'''


def subscript_it(string: str) -> str:
    '''
    Turns `5` into `₅`
    '''

    subs = '₀₁₂₃₄₅₆₇₈₉'

    res: list[str] = []

    for char in string:
        if char.isdigit():
            res.append(subs[int(char)])
        else:
            res.append(char)

    return ''.join(res)


def clean_str(string: str, chars_to_del: str):
    '''
    Deletes all unnecessary characters
    '''
    res = []

    for char in string:
        if not char in chars_to_del:
            res.append(char)

    return ''.join(res)


def clean_ws(string: str) -> str:
    '''
    Deletes all unnecessary whitespaces and other garbage
    '''
    return clean_str(string, ' \f\n\r\t\v\u00a0\u1680\u2000\u200a\u2028\u2029\u202f\u205f\u3000\ufeff')

import argparse
from math import ceil


RUSSIAN_DICT = {
    'А': '1',
    'Б': '81', 
    'В': '82', 
    'Г': '83', 
    'Д': '84', 
    'Е': '4', 
    'Ж': '85', 
    'З': '86', 
    'И': '2', 
    'К': '87', 
    'Л': '88', 
    'М': '89',
    'Н': '6',
    'О': '7', 
    'П': '80',
    'Р': '91',
    'С': '5',
    'Т': '3',
    'У': '92',
    'Ф': '93',
    'Х': '94',
    'Ц': '95',
    'Ч': '96',
    'Ш': '97',
    'Щ': '98',
    'Ъ': '99',
    'Ы': '90',
    'Ь': '01',
    'Э': '02',
    'Ю': '03',
    'Я': '04',
    ' ': '00'
}


def translate(text, rules=RUSSIAN_DICT):
    return ''.join([rules[ch] for ch in text])


def reverse_translate(code, rules=RUSSIAN_DICT):
    rules = dict(zip(rules.values(), rules.keys()))
    carry = ''
    result = []
    for ch in code:
        value = rules.get(f'{carry}{ch}')
        if value is not None:
            result.append(value)
            carry = ''
        else:
            carry = ch

    return ''.join(result)


def encode(code, key):
    code, key = add_padding(code, key)

    res = []
    for i in range(len(code)):
        res.append(str((int(code[i]) + int(key[i])) % 10))
    
    return ''.join(res)


def decode(code, key):
    code, key = add_padding(code, key)

    res = []
    for i in range(len(code)):
        res.append(str((10 + int(code[i]) - int(key[i])) % 10))
    
    return ''.join(res)


def add_padding(code, key):
    if len(code) > len(key):
        key = key * ceil(len(code) / len(key))

    code = code.ljust(len(key), '0')

    return code, key


def main(text, key, decrypt):
    key_code = translate(key)

    if not decrypt:
        text_code = translate(text)
        res = encode(text_code, key_code)
    else:
        decoded = decode(text, key_code)
        res = reverse_translate(decoded)

    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run encryption.')
    parser.add_argument(
        '-t', '--text', required=True, dest='text', help='Text to enctrypt.'
    )
    parser.add_argument(
        '-k', '--key', required=True, dest='key', help='Key for encryption.'
    )
    parser.add_argument(
        '-d', '--decrypt', dest='decrypt', default=False, action='store_true'
    )

    args = parser.parse_args()
    res = main(args.text, args.key, args.decrypt)

    print(res)

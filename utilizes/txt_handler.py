import json


def save_txt(link, content, handle_type):
    """a: append
       w: write"""
    try:
        f = open(link, handle_type, encoding='utf-8')
        f.write(content)
        f.close()
        return None
    except Exception as e:
        return e


def load_txt(path):
    try:
        f = open(path, 'r', encoding='utf8')
        data = f.read()
        f.close()
        return data
    except Exception as e:
        print(f'Lỗi method load_txt: {e}')
        return None


def read_txt(path):
    return load_txt(path)


def read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        f.close()
        return data
    except Exception as e:
        print('Lỗi khi read json', e)
        return {}


def write_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

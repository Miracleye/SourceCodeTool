import codecs
import os


def open_file(file):
    if not os.path.isfile(file):
        return None
    f = codecs.open(file, encoding='utf-8')
    try:
        text = f.read()
        return text
    except Exception:
        return None
    finally:
        f.close()


def save_file(file, text):
    if not os.path.isfile(file):
        raise FileNotFoundError()
    f = codecs.open(file, mode='w+', encoding='utf-8')
    try:
        f.write(text)
    except IOError as err:
        raise err
    finally:
        f.close()

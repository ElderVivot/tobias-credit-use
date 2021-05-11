import json
import platform
from codecs import open


def readJson(filePath: str) -> dict:
    try:
        if platform.system() == 'Windows':
            with open(filePath, 'rb', encoding='latin1') as file:
                return json.load(file)
        else:
            with open(filePath, 'rb') as file:
                return json.load(file)
    except Exception as e:
        print(e)
        return {}

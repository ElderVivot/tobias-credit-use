import json
from codecs import open


def readJson(filePath: str) -> dict:
    try:
        with open(filePath, 'r', encoding='latin1') as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}

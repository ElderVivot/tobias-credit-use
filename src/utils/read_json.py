import json
import codecs


def readJson(filePath: str) -> dict:
    try:
        with codecs.open(filePath, 'r', 'latin1') as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}

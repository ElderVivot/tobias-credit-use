import json


def readJson(filePath: str) -> dict:
    try:
        with open(filePath) as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return {}

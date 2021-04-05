import os
import sys
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)


class SaveData(object):
    def __init__(self, connection: Database, nameCollection: str):
        self._connection = connection
        self._nameCollection = nameCollection
        self._collection: Collection = self._connection[self._nameCollection]

    def save(self, data: Dict[str, str], filters: Dict[str, str]):
        try:
            self._collection.update_one(
                filters,
                {"$set": data},
                upsert=True
            )
        except Exception as e:
            print(f"** Error to save data. The message is: {e}")

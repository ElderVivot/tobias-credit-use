import os
import sys
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import ASCENDING
from typing import Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)


class SaveData(object):
    def __init__(self, connection: Database, nameCollection: str):
        self._connection = connection
        self._nameCollection = nameCollection
        self._collection: Collection = self._connection[self._nameCollection]
        self._createIndex()

    def _createIndex(self):
        indexes = list(self._collection.index_information())
        if len(indexes) <= 1:
            self._collection.create_index([
                ("chave_nota", ASCENDING),
                ("prod_numero_item", ASCENDING)
            ])

    def save(self, data: Dict[str, str], filters: Dict[str, str]):
        try:
            self._collection.update_one(
                filters,
                {"$set": data},
                upsert=True
            )
        except Exception as e:
            print(f"** Error to save data. The message is: {e}")

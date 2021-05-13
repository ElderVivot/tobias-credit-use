import os
import sys
from pymongo.database import Database
from pymongo.collection import Collection
from typing import List, Dict, Union

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)


class GetListProduct(object):
    def __init__(self, connection: Database, nameCollection: str):
        self._connection = connection
        self._nameCollection = nameCollection
        self._collection: Collection = self._connection[self._nameCollection]

    def getList(self) -> Union[List[Dict[str, str]], None]:
        try:
            listProducts: List[Dict[str, str]] = self._collection.find()
            return listProducts
        except Exception as e:
            print(f"** Error to get data. The message is: {e}")
            return None


if __name__ == '__main__':
    from dao.connect_mongo import ConnectMongoDB

    connectMongo = ConnectMongoDB()
    connection = connectMongo.getConnetion()

    main = GetListProduct(connection, 'notas_14437943000271')
    # [print(obj) for obj in main.getList()]

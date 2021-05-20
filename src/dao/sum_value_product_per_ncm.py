import os
import sys
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)


class SumValueProductPerNcm(object):
    def __init__(self, connection: Database, nameCollection: str):
        self._connection = connection
        self._nameCollection = nameCollection
        self._collection: Collection = self._connection[self._nameCollection]

    def getSum(self):
        try:
            sumPerNcmRule: Dict[str, str] = self._collection.aggregate([
                {
                    "$group": {
                        "_id": {
                            "prod_ncm": "$prod_ncm",
                            "prod_name_ncm": "$prod_name_ncm",
                            "prod_ncm_rule": "$prod_ncm_rule"
                        },
                        "sumTotal": {"$sum": "$prod_valor_total"},
                        "qtdTotal": {"$sum": 1}
                    }
                }
            ])
            return sumPerNcmRule
        except Exception as e:
            print(f"** Error to save data. The message is: {e}")


if __name__ == '__main__':
    from dao.connect_mongo import ConnectMongoDB

    connectMongo = ConnectMongoDB()
    connection = connectMongo.getConnetion()

    main = SumValueProductPerNcm(connection, 'notas_14437943000271')
    # [print(obj) for obj in main.getSum()]

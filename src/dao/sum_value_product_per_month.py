import os
import sys
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)


class SumValueProductPerMonth(object):
    def __init__(self, connection: Database, nameCollection: str, year: int, month: int):
        self._connection = connection
        self._nameCollection = nameCollection
        self._collection: Collection = self._connection[self._nameCollection]
        self._year = year
        self._month = month

    def getSum(self):
        try:
            sumPerNcmRule: Dict[str, str] = self._collection.aggregate([
                {
                    "$match": {
                        "$and": [{"month_emissao": self._month}, {"year_emissao": self._year}]
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "prod_ncm_rule": "$prod_ncm_rule"
                        },
                        "sumTotal": {"$sum": "$prod_valor_total"}
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

    main = SumValueProductPerMonth(connection, 'notas_14437943000271', 2017, 10)
    # [print(obj) for obj in main.getSum()]

import os
import sys
from pymongo import MongoClient
from pymongo.database import Database

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.read_json import readJson

envJson = readJson(os.path.join(dirNameSrc, '..', 'env.json'))


class ConnectMongoDB(object):
    def __init__(self, nameDB='tobias'):
        self._connection: MongoClient = None
        self._selectDB: Database = None
        self._nameDB = nameDB

    def getConnetion(self) -> Database:
        if self._connection is None:
            try:
                self._connection = MongoClient(envJson['url_mongo'])
                self._selectDB = self._connection[self._nameDB]
            except Exception as e:
                print(f"** Não foi possível realizar a conexão. O erro é: {e}")
                return None
        return self._selectDB

    def closeConnection(self) -> None:
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception as e:
                print(f"** Não foi possível fechar a conexão. O erro é: {e}")

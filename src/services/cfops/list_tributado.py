import os
import sys
from typing import List

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.read_txt import readTxt


class ListCfopTributado():
    def __init__(self) -> None:
        self._fileListCfopTributado = os.path.join(dirNameSrc, '..', 'data', 'cfops', 'tributado.txt')
        self._dataTxt = readTxt(self._fileListCfopTributado)
        self._listNcm: List[int] = []

    def getList(self) -> List[int]:
        for data in self._dataTxt:
            cfop = int(data)
            if cfop > 0:
                self._listNcm.append(cfop)
        return self._listNcm


if __name__ == '__main__':
    main = ListCfopTributado()
    print(main.getList())

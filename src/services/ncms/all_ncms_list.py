import os
import sys
from typing import Dict, Union

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsText


class AllNcmsList():
    def __init__(self, dataNcm: dict):
        self._dataNcm: dict = dataNcm

    def process(self) -> Union[Dict[str, str], None]:
        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['exportacao', ncm]))
        if nameNcm != "":
            return {
                "ncm": ncm,
                "nameNcm": nameNcm
            }
        else:
            nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['importacao', ncm]))
            if nameNcm != "":
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm
                }
            return None

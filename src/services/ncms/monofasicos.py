import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsText


class Monofasicos():
    def __init__(self, dataNcm: dict):
        self._dataNcm: dict = dataNcm

    def monofasicoVarejo(self):
        tagsNecessaries = ['monofasico_varejo']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['monofasico_varejo', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            return {
                "ncm": ncm,
                "nameNcm": nameNcm,
                "tag": 'MonofasicoVarejo',
                "dataTag": ""
            }

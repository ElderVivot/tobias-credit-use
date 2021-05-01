import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsText


class Monofasicos():
    def __init__(self, dataNcm: dict, returnOnlyValueNcm=False):
        self._dataNcm: dict = dataNcm
        self._returnOnlyValueNcm = returnOnlyValueNcm

    def monofasicoVarejo(self):
        tagsNecessaries = ['monofasico_varejo']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['monofasico_varejo', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            if self._returnOnlyValueNcm is False:
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm,
                    "tag": 'MonofasicoVarejo',
                    "dataTag": ""
                }
            else:
                return ncm

    def monofasicoAtacadoSN_CST_4(self):
        tagsNecessaries = ['monofasico_atacado', 'codigo_da_situacao_tributaria_cst', 'simples_nacional', 'saida', '4']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['monofasico_atacado', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            if self._returnOnlyValueNcm is False:
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm,
                    "tag": 'MonofasicoAtacadoSN_CST_4',
                    "dataTag": ""
                }
            else:
                return ncm

    def monofasicoAtacadoSN_CST_6(self):
        tagsNecessaries = ['monofasico_atacado', 'codigo_da_situacao_tributaria_cst', 'simples_nacional', 'saida', '6']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['monofasico_atacado', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            if self._returnOnlyValueNcm is False:
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm,
                    "tag": 'MonofasicoAtacadoSN_CST_6',
                    "dataTag": ""
                }
            else:
                return ncm

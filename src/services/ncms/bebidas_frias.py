import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(dirNameSrc)

from utils.functions import returnDataInDictOrArray, treatsFieldAsText


class BebidasFrias():
    def __init__(self, dataNcm: dict, returnOnlyValueNcm=False):
        self._dataNcm: dict = dataNcm
        self._returnOnlyValueNcm = returnOnlyValueNcm

    def bebidaFria(self):
        tagsNecessaries = ['bebidas_frias']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['bebidas_frias', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            if self._returnOnlyValueNcm is False:
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm,
                    "tag": 'BebidaFria',
                    "dataTag": ""
                }
            else:
                return ncm

    def cstSNVendaVarejista(self):
        tagsNecessaries = ['bebidas_frias', 'codigo_da_situacao_tributaria_cst', 'simples_nacional',
                           'saida_(venda_pelo_comercio_varejista)']

        ncm = self._dataNcm['ncm']
        nameNcm = treatsFieldAsText(returnDataInDictOrArray(self._dataNcm, ['bebidas_frias', ncm]))
        dataTagsNecessaries = returnDataInDictOrArray(self._dataNcm, tagsNecessaries, None)
        if dataTagsNecessaries is not None:
            if self._returnOnlyValueNcm is False:
                return {
                    "ncm": ncm,
                    "nameNcm": nameNcm,
                    "tag": 'BebidaFria_CST_SN_SaidaVendaComercioVarejista',
                    "dataTag": dataTagsNecessaries
                }
            else:
                return ncm

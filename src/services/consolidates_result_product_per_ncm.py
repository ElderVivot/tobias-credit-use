import os
import sys
from typing import Dict, List

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from dao.sum_value_product_per_ncm import SumValueProductPerNcm
from dao.connect_mongo import ConnectMongoDB


class ConsolidatesResultProductPerNcm():
    def __init__(self, inscricaoFederal: str):
        self._inscricaoFederal = inscricaoFederal

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()
        self._listSumObj: List[Dict[str, str]] = []
        self._sumObj: Dict[str, str] = {}

    def __groupByPerNcm(self) -> None:
        findThisNcm = False
        for index, sumObj in enumerate(self._listSumObj):
            if sumObj['prod_ncm'] == self._sumObj['prod_ncm']:
                findThisNcm = True
                self._listSumObj[index]['qtdTotal'] += self._sumObj['qtdTotal']
                self._listSumObj[index]['tributado'] += self._sumObj['tributado']
                self._listSumObj[index]['monofasico_varejo'] += self._sumObj['monofasico_varejo']
                self._listSumObj[index]['bebida_fria'] += self._sumObj['bebida_fria']
                self._listSumObj[index]['monofasico_atacado'] += self._sumObj['monofasico_atacado']
                self._listSumObj[index]['cfop_nao_tributado'] += self._sumObj['cfop_nao_tributado']

        if findThisNcm is False:
            self._listSumObj.append(self._sumObj.copy())

    def consolidate(self):
        sumValueProduct = SumValueProductPerNcm(self._database, f"notas_{self._inscricaoFederal}")
        getSums = sumValueProduct.getSum()
        for getSum in getSums:
            prodNcmRule = getSum['_id']['prod_ncm_rule']

            self._sumObj['emitente_inscricao_federal'] = self._inscricaoFederal
            self._sumObj['prod_ncm'] = getSum['_id']['prod_ncm']
            self._sumObj['prod_name_ncm'] = getSum['_id']['prod_name_ncm']
            self._sumObj['quantidade_deste_ncm'] = getSum['qtdTotal']
            self._sumObj['cfop_nao_tributado'] = 0
            self._sumObj['tributado'] = 0
            self._sumObj['monofasico_varejo'] = 0
            self._sumObj['bebida_fria'] = 0
            self._sumObj['monofasico_atacado'] = 0

            if prodNcmRule == 'CFOPNaoTributado':
                self._sumObj['cfop_nao_tributado'] = getSum['sumTotal']
            elif prodNcmRule == '':
                self._sumObj['tributado'] = getSum['sumTotal']
            elif prodNcmRule == 'MonofasicoVarejo':
                self._sumObj['monofasico_varejo'] = getSum['sumTotal']
            elif prodNcmRule == 'BebidaFria':
                self._sumObj['bebida_fria'] = getSum['sumTotal']
            elif prodNcmRule == 'MonofasicoAtacadoSN_CST_4' or prodNcmRule == 'MonofasicoAtacadoSN_CST_6':
                self._sumObj['monofasico_atacado'] = getSum['sumTotal']

            self.__groupByPerNcm()
            self._sumObj.clear()

        return self._listSumObj

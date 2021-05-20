import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from dao.sum_value_product_per_ncm import SumValueProductPerNcm
from dao.connect_mongo import ConnectMongoDB


class ConsolidatesResultProductPerNcm():
    def __init__(self, inscricaoFederal: str):
        self._inscricaoFederal = inscricaoFederal

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

    def consolidate(self):
        listSumObj = []
        sumObj = {}
        sumObj['emitente_inscricao_federal'] = self._inscricaoFederal
        sumObj['prod_ncm'] = ''
        sumObj['prod_name_ncm'] = ''
        sumObj['tributado'] = 0
        sumObj['monofasico_varejo'] = 0
        sumObj['bebida_fria'] = 0
        sumObj['monofasico_atacado'] = 0

        sumValueProduct = SumValueProductPerNcm(self._database, f"notas_{self._inscricaoFederal}")
        getSums = sumValueProduct.getSum()
        for getSum in getSums:
            prodNcmRule = getSum['_id']['prod_ncm_rule']

            sumObj['prod_ncm'] = getSum['_id']['prod_ncm']
            sumObj['prod_name_ncm'] = getSum['_id']['prod_name_ncm']

            if prodNcmRule == '':
                sumObj['tributado'] = getSum['sumTotal']
            elif prodNcmRule == 'MonofasicoVarejo':
                sumObj['monofasico_varejo'] = getSum['sumTotal']
            elif prodNcmRule == 'BebidaFria':
                sumObj['bebida_fria'] = getSum['sumTotal']
            elif prodNcmRule == 'MonofasicoAtacadoSN_CST_4' or prodNcmRule == 'MonofasicoAtacadoSN_CST_6':
                sumObj['monofasico_atacado'] += getSum['sumTotal']

        listSumObj.append(sumObj.copy())

        return listSumObj

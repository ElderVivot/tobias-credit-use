import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnMonthsOfYear
from dao.sum_value_product_per_month import SumValueProductPerMonth
from dao.connect_mongo import ConnectMongoDB


class ConsolidatesResultProductPerMonth():
    def __init__(self, inscricaoFederal: str, monthStart: int, yearStart: int, monthEnd: int, yearEnd: int):
        self._inscricaoFederal = inscricaoFederal
        self._monthStart = monthStart
        self._yearStart = yearStart
        self._monthEnd = monthEnd
        self._yearEnd = yearEnd

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

    def consolidate(self):
        listSumObj = []
        year = self._yearStart
        while year <= self._yearEnd:
            months = returnMonthsOfYear(year, self._monthStart, self._yearStart, self._monthEnd, self._yearEnd)

            # print('\t - ', end='')
            for month in months:
                monthYearStr = f'{month:0>2}/{year}'
                # print(monthYearStr, ' ', end='')

                sumObj = {}
                sumObj['emitente_inscricao_federal'] = self._inscricaoFederal
                sumObj['competence'] = f'01/{monthYearStr}'
                sumObj['tributado'] = 0
                sumObj['monofasico_varejo'] = 0
                sumObj['bebida_fria'] = 0
                sumObj['monofasico_atacado'] = 0

                sumValueProduct = SumValueProductPerMonth(self._database, f"notas_{self._inscricaoFederal}", year, month)
                getSums = sumValueProduct.getSum()
                for getSum in getSums:
                    prodNcmRule = getSum['_id']['prod_ncm_rule']

                    if prodNcmRule == '':
                        sumObj['tributado'] = getSum['sumTotal']
                    elif prodNcmRule == 'MonofasicoVarejo':
                        sumObj['monofasico_varejo'] = getSum['sumTotal']
                    elif prodNcmRule == 'BebidaFria':
                        sumObj['bebida_fria'] = getSum['sumTotal']
                    elif prodNcmRule == 'MonofasicoAtacadoSN_CST_4' or prodNcmRule == 'MonofasicoAtacadoSN_CST_6':
                        sumObj['monofasico_atacado'] += getSum['sumTotal']

                listSumObj.append(sumObj.copy())

            # print('')
            year += 1

        return listSumObj

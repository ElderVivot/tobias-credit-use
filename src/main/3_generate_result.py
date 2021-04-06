import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import returnMonthsOfYear, getDateTimeNowInFormatStr
from dao.sum_value_product import SumValueProduct
from dao.connect_mongo import ConnectMongoDB


class GenerateResult():
    def __init__(self, inscricaoFederal: str, monthStart: int, yearStart: int, monthEnd: int, yearEnd: int):
        self._inscricaoFederal = inscricaoFederal
        self._monthStart = monthStart
        self._yearStart = yearStart
        self._monthEnd = monthEnd
        self._yearEnd = yearEnd

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

        self._folderSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed',
                                              'resultado_analise', f'{getDateTimeNowInFormatStr()}.csv')
        self._writeHeader()

    def _writeHeader(self):
        with open(self._folderSaveResult, 'w') as file:
            file.write("Competencia;Tributado;Monofasico Varejo;Bebidas Frias\n")

    def _saveResult(self, sumObj):
        with open(self._folderSaveResult, 'a') as file:
            file.write(f"{sumObj['competence']};{sumObj['tributado']};{sumObj['monofasico_varejo']};{sumObj['bebida_fria']}\n")

    def process(self):
        year = self._yearStart
        while year <= self._yearEnd:
            months = returnMonthsOfYear(year, monthStart, yearStart, monthEnd, yearEnd)

            print('\t - ', end='')
            for month in months:
                monthYearStr = f'{month:0>2}/{year}'
                print(monthYearStr, ' ', end='')

                sumObj = {}
                sumObj['competence'] = f'01/{monthYearStr}'
                sumObj['tributado'] = 0
                sumObj['monofasico_varejo'] = 0
                sumObj['bebida_fria'] = 0

                sumValueProduct = SumValueProduct(self._database, f"nfe_{self._inscricaoFederal}", year, month)
                getSums = sumValueProduct.getSum()
                for getSum in getSums:
                    if getSum['_id'] == '':
                        sumObj['tributado'] = getSum['sumTotal']
                    elif getSum['_id'] == 'MonofasicoVarejo':
                        sumObj['monofasico_varejo'] = getSum['sumTotal']
                    elif getSum['_id'] == 'BebidaFria':
                        sumObj['bebida_fria'] = getSum['sumTotal']

                self._saveResult(sumObj)

            print('')
            year += 1


if __name__ == '__main__':
    inscricaoFederal = str(sys.argv[1])
    monthStart = int(sys.argv[2])
    yearStart = int(sys.argv[3])
    monthEnd = int(sys.argv[4])
    yearEnd = int(sys.argv[5])

    main = GenerateResult(inscricaoFederal, monthStart, yearStart, monthEnd, yearEnd)
    main.process()
import os
import sys
import pandas as pd

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import getDateTimeNowInFormatStr
from services.consolidates_result import ConsolidatesResult
from dao.connect_mongo import ConnectMongoDB
from dao.get_list_product import GetListProduct


class GenerateResult():
    def __init__(self, inscricaoFederal: str, monthStart: int, yearStart: int, monthEnd: int, yearEnd: int):
        self._inscricaoFederal = inscricaoFederal
        self._monthStart = monthStart
        self._yearStart = yearStart
        self._monthEnd = monthEnd
        self._yearEnd = yearEnd

        self._consolidateResult = ConsolidatesResult(self._inscricaoFederal, self._monthStart, self._yearStart,
                                                     self._monthEnd, self._yearEnd)
        self._listSumObj = self._consolidateResult.consolidate()

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

        self._getListProduct = GetListProduct(self._database, f"notas_{self._inscricaoFederal}")
        self._listProduct = self._getListProduct.getList()

        self._folderSaveResultResume = os.path.join(dirNameSrc, '..', 'data', 'processed',
                                                    'resultado_analise',
                                                    f'resumo_{self._inscricaoFederal}_{getDateTimeNowInFormatStr()}.xlsx')
        self._folderSaveResultDetailed = os.path.join(dirNameSrc, '..', 'data', 'processed',
                                                      'resultado_analise',
                                                      f'detalhado_{self._inscricaoFederal}_{getDateTimeNowInFormatStr()}.xlsx')

    def _saveResult(self):
        print('\t - Salvando resultado.')
        dfListSumObj = pd.DataFrame(self._listSumObj)
        dfListSumObj.to_excel(self._folderSaveResultResume,
                              header=['Competência', 'Tributado', 'Monofásico Varejo', 'Bebidas Frias', 'Monofásico Atacado'],
                              index=False, float_format="%.2f")
        dfListProduct = pd.DataFrame(self._listProduct)
        dfListProduct.to_excel(self._folderSaveResultDetailed, index=False, float_format="%.2f")

    def process(self):
        self._saveResult()


if __name__ == '__main__':
    inscricaoFederal = str(sys.argv[1])
    monthStart = int(sys.argv[2])
    yearStart = int(sys.argv[3])
    monthEnd = int(sys.argv[4])
    yearEnd = int(sys.argv[5])

    main = GenerateResult(inscricaoFederal, monthStart, yearStart, monthEnd, yearEnd)
    main.process()

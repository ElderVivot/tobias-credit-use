import os
import sys
import pandas as pd

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)
foderToSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed', 'resultado_analise')

from utils.functions import getDateTimeNowInFormatStr
from services.consolidates_result_product_per_month import ConsolidatesResultProductPerMonth
from services.consolidates_result_product_per_ncm import ConsolidatesResultProductPerNcm
from dao.connect_mongo import ConnectMongoDB
from services.save_products_in_excel import SaveProductsInExcel


class GenerateResult():
    def __init__(self, inscricaoFederal: str, monthStart: int, yearStart: int, monthEnd: int, yearEnd: int):
        self._inscricaoFederal = inscricaoFederal
        self._monthStart = monthStart
        self._yearStart = yearStart
        self._monthEnd = monthEnd
        self._yearEnd = yearEnd

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

        self.__instanceDatasToSave()
        self.__folderToSaveData()

    def __instanceDatasToSave(self):
        self._consolidateResultProductPerMonth = ConsolidatesResultProductPerMonth(
            self._inscricaoFederal, self._monthStart, self._yearStart,
            self._monthEnd, self._yearEnd
        )

        self._consolidateResultProductPerNcm = ConsolidatesResultProductPerNcm(self._inscricaoFederal)

        self._saveProductsInExcel = SaveProductsInExcel(self._inscricaoFederal, self._monthStart, self._yearStart,
                                                        self._monthEnd, self._yearEnd)

    def __folderToSaveData(self):
        self._folderSaveResultResumeProductPerMonth = os.path.join(
            foderToSaveResult,
            f'resumo_por_competencia_{self._inscricaoFederal}_{getDateTimeNowInFormatStr()}.xlsx'
        )
        self._folderSaveResultResumeProductPerNcm = os.path.join(
            foderToSaveResult,
            f'resumo_por_ncm_{self._inscricaoFederal}_{getDateTimeNowInFormatStr()}.xlsx'
        )

    def _saveResult(self):
        print('\t- Salvando resultados.')

        print('\t\t- Consolidado por mês')
        self._listSumResultProductPerMonth = self._consolidateResultProductPerMonth.consolidate()
        dfListSumObjProductPerMonth = pd.DataFrame(self._listSumResultProductPerMonth)
        dfListSumObjProductPerMonth.to_excel(
            self._folderSaveResultResumeProductPerMonth,
            header=['CNPJ', 'Competência', 'Tributado', 'Monofásico Varejo', 'Bebidas Frias', 'Monofásico Atacado'],
            index=False, float_format="%.2f"
        )

        print('\t\t- Consolidado por NCM')
        self._listSumResultProductPerNcm = self._consolidateResultProductPerNcm.consolidate()
        dfListSumResultProductPerNcm = pd.DataFrame(self._listSumResultProductPerNcm)
        dfListSumResultProductPerNcm.to_excel(
            self._folderSaveResultResumeProductPerNcm,
            header=['CNPJ', 'NCM', 'Nome NCM', 'Quantidade deste Ncm', 'Tributado',
                    'Monofásico Varejo', 'Bebidas Frias', 'Monofásico Atacado'],
            index=False, float_format="%.2f"
        )

        print('\t\t- Lista de Produtos')
        self._saveProductsInExcel.saveData()

    def process(self):
        # pass
        self._saveResult()


if __name__ == '__main__':
    inscricaoFederal = str(sys.argv[1])
    monthStart = int(sys.argv[2])
    yearStart = int(sys.argv[3])
    monthEnd = int(sys.argv[4])
    yearEnd = int(sys.argv[5])

    main = GenerateResult(inscricaoFederal, monthStart, yearStart, monthEnd, yearEnd)
    main.process()

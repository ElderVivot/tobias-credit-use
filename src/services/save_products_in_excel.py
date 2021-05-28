import os
import sys
from typing import Dict, List
from xlsxwriter import Workbook

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)
foderToSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed', 'resultado_analise')

from dao.connect_mongo import ConnectMongoDB
from utils.functions import returnMonthsOfYear, getDateTimeNowInFormatStr, treatsFieldAsDateInDictOrArray, \
    treatsFieldAsNumberInDictOrArray, treatsFieldAsTextInDictOrArray, \
    treatsFieldAsDecimalInDictOrArray
from dao.get_list_product import GetListProduct


class SaveProductsInExcel():
    def __init__(self, inscricaoFederal: str, monthStart: int, yearStart: int, monthEnd: int, yearEnd: int):
        self._inscricaoFederal = inscricaoFederal
        self._monthStart = monthStart
        self._yearStart = yearStart
        self._monthEnd = monthEnd
        self._yearEnd = yearEnd

        self._connectMongo = ConnectMongoDB()
        self._database = self._connectMongo.getConnetion()

        self._workbook = Workbook(os.path.join(
            foderToSaveResult,
            f'detalhado_{self._inscricaoFederal}_{getDateTimeNowInFormatStr()}.xlsx'
        ))
        self._sheet = self._workbook.add_worksheet('Produtos')
        self.__setSettingsOfWorkbook()
        self.__writeReader()
        self._row = 0

    def __setSettingsOfWorkbook(self):
        self._cell_format_header = self._workbook.add_format(
            {'bold': True, 'font_color': 'black', 'bg_color': 'yellow', 'text_wrap': True})
        self._cell_format_money = self._workbook.add_format({'num_format': '##0.00'})
        self._cell_format_date = self._workbook.add_format({'num_format': 'dd/mm/yyyy'})

    def __writeReader(self):
        self._sheet.write(0, 0, "CNPJ Emitente", self._cell_format_header)
        self._sheet.write(0, 1, "Nome Emitente", self._cell_format_header)
        self._sheet.write(0, 2, "Numero NF", self._cell_format_header)
        self._sheet.write(0, 3, "Data Emissao", self._cell_format_header)
        self._sheet.write(0, 4, "Modelo NF", self._cell_format_header)
        self._sheet.write(0, 5, "Serie", self._cell_format_header)
        self._sheet.write(0, 6, "CNPJ Destinatario", self._cell_format_header)
        self._sheet.write(0, 7, "Nome Destinatario", self._cell_format_header)
        self._sheet.write(0, 8, "Chave Nota", self._cell_format_header)
        self._sheet.write(0, 9, "Cod. Produto", self._cell_format_header)
        self._sheet.write(0, 10, "Nome Produto", self._cell_format_header)
        self._sheet.write(0, 11, "NCM", self._cell_format_header)
        self._sheet.write(0, 12, "Nome NCM", self._cell_format_header)
        self._sheet.write(0, 13, "Regra aplicada pra este NCM", self._cell_format_header)
        self._sheet.write(0, 14, "Unidade", self._cell_format_header)
        self._sheet.write(0, 15, "CFOP", self._cell_format_header)
        self._sheet.write(0, 16, "Quantidade", self._cell_format_header)
        self._sheet.write(0, 17, "Valor Unitario", self._cell_format_header)
        self._sheet.write(0, 18, "Valor Produto", self._cell_format_header)
        self._sheet.write(0, 19, "Valor Desconto", self._cell_format_header)
        self._sheet.write(0, 20, "Valor Frete", self._cell_format_header)
        self._sheet.write(0, 21, "Valor Outros", self._cell_format_header)
        self._sheet.write(0, 22, "Valor VSeg", self._cell_format_header)
        self._sheet.write(0, 23, "Valor Total", self._cell_format_header)

    def __writeRows(self, product: Dict[str, str]) -> None:
        emitenteInscricaoFederal = treatsFieldAsTextInDictOrArray(product, ['emitente_inscricao_federal'])
        emitenteRazaoSocial = treatsFieldAsTextInDictOrArray(product, ['emitente_razao_social'])
        numeroNF = treatsFieldAsNumberInDictOrArray(product, ['identificao_nfe_numero_nf'])
        dataEmissaoNF = treatsFieldAsDateInDictOrArray(product, ['identificao_nfe_data_emissao'], formatoData=2)
        modeloNF = treatsFieldAsTextInDictOrArray(product, ['identificao_nfe_modelo_nf'])
        serieNF = treatsFieldAsTextInDictOrArray(product, ['identificao_nfe_serie_nf'])
        destinatarioInscricaoFederal = treatsFieldAsTextInDictOrArray(product, ['destinatario_inscricao_federal'])
        destinatarioRazaoSocial = treatsFieldAsTextInDictOrArray(product, ['destinatario_razao_social'])
        chaveNota = treatsFieldAsTextInDictOrArray(product, ['chave_nota'])
        codigoProduto = treatsFieldAsTextInDictOrArray(product, ['prod_codigo_produto'])
        nomeProduto = treatsFieldAsTextInDictOrArray(product, ['prod_nome_produto'])
        ncm = treatsFieldAsTextInDictOrArray(product, ['prod_ncm'])
        nomeNCM = treatsFieldAsTextInDictOrArray(product, ['prod_name_ncm'])
        ruleNCM = treatsFieldAsTextInDictOrArray(product, ['prod_ncm_rule'])
        unidade = treatsFieldAsTextInDictOrArray(product, ['prod_unidade'])
        cfop = treatsFieldAsNumberInDictOrArray(product, ['prod_cfop'])
        quantidade = treatsFieldAsDecimalInDictOrArray(product, ['prod_quantidade'])
        valorUnitario = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_unitario'])
        valorProduto = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_produto'])
        valorDesconto = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_desconto'])
        valorFrete = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_frete'])
        valorOutros = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_outros'])
        valorVSeg = treatsFieldAsDecimalInDictOrArray(product, ['prod_vseg'])
        valorTotal = treatsFieldAsDecimalInDictOrArray(product, ['prod_valor_total'])

        self._sheet.write(self._row, 0, emitenteInscricaoFederal)
        self._sheet.write(self._row, 1, emitenteRazaoSocial)
        self._sheet.write(self._row, 2, numeroNF)
        self._sheet.write(self._row, 3, dataEmissaoNF, self._cell_format_date)
        self._sheet.write(self._row, 4, modeloNF)
        self._sheet.write(self._row, 5, serieNF)
        self._sheet.write(self._row, 6, destinatarioInscricaoFederal)
        self._sheet.write(self._row, 7, destinatarioRazaoSocial)
        self._sheet.write(self._row, 8, chaveNota)
        self._sheet.write(self._row, 9, codigoProduto)
        self._sheet.write(self._row, 10, nomeProduto)
        self._sheet.write(self._row, 11, ncm)
        self._sheet.write(self._row, 12, nomeNCM)
        self._sheet.write(self._row, 13, ruleNCM)
        self._sheet.write(self._row, 14, unidade)
        self._sheet.write(self._row, 15, cfop)
        self._sheet.write(self._row, 16, quantidade)
        self._sheet.write(self._row, 17, valorUnitario, self._cell_format_money)
        self._sheet.write(self._row, 18, valorProduto, self._cell_format_money)
        self._sheet.write(self._row, 19, valorDesconto, self._cell_format_money)
        self._sheet.write(self._row, 20, valorFrete, self._cell_format_money)
        self._sheet.write(self._row, 21, valorOutros, self._cell_format_money)
        self._sheet.write(self._row, 22, valorVSeg, self._cell_format_money)
        self._sheet.write(self._row, 23, valorTotal, self._cell_format_money)

    def __closeWorkbook(self):
        self._workbook.close()

    def saveData(self):
        year = self._yearStart
        while year <= self._yearEnd:
            months = returnMonthsOfYear(year, self._monthStart, self._yearStart, self._monthEnd, self._yearEnd)

            print('\t\t\t- ', end='')
            for month in months:
                monthYearStr = f'{month:0>2}/{year}'
                print(monthYearStr, ' ', end='')

                getListProduct = GetListProduct(self._database, f"notas_{self._inscricaoFederal}", year, month)
                listProducts: List[Dict[str, str]] = getListProduct.getList()
                for product in listProducts:
                    self._row += 1
                    self.__writeRows(product)

            print('')
            year += 1

        self.__closeWorkbook()


if __name__ == '__main__':
    main = SaveProductsInExcel('14437943000271', 4, 2016, 4, 2021)
    main.saveData()

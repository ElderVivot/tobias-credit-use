import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from typing import List, Dict


class CompareXmlXNcmRules():
    def __init__(self, dataXml: Dict[str, dict], listNcm: List[str], folderSaveResult: str):
        self._dataXml = dataXml
        self._listNcm = listNcm
        self._folderSaveResult = folderSaveResult

    def _checkIfNcmInList(self, ncm):
        return True if self._listNcm.count(ncm) > 0 else False

    def process(self):
        for index, product in enumerate(self._dataXml['dados_produtos']):
            product['nmc_in_list_rule'] = self._checkIfNcmInList(product['ncm'])
            self._saveResult(product)

    def _saveResult(self, product):
        with open(self._folderSaveResult, 'a') as file:
            file.write(f"{self._dataXml['identificao_nfe']['numero_nf']};{self._dataXml['identificao_nfe']['modelo_nf']};{self._dataXml['identificao_nfe']['serie_nf']};{self._dataXml['identificao_nfe']['data_emissao']};'{self._dataXml['emitente']['inscricao_federal']};{self._dataXml['emitente']['razao_social']};'{self._dataXml['destinatario']['inscricao_federal']};{self._dataXml['destinatario']['razao_social']};'{product['codigo_produto']};\"{product['nome_produto']}\";'{product['ncm']};{product['cfop']};{product['unidade']};{product['quantidade']};{product['valor_unitario']};{product['valor_total']};{product['nmc_in_list_rule']};'{self._dataXml['chave_nota']}\n")

import os
import sys
from typing import List, Dict
from pymongo.database import Database

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from dao.save_data import SaveData
from utils.functions import treatsFieldAsDate


class CompareXmlXNcmRules():
    def __init__(self, database: Database, dataXml: Dict[str, dict], listNcm: List[str], folderSaveResult: str):
        self._database = database
        self._dataXml = dataXml
        self._listNcm = listNcm
        self._folderSaveResult = folderSaveResult

        inscricaoFederal = self._dataXml['emitente']['inscricao_federal']
        self._saveData = SaveData(self._database, f'nfe_{inscricaoFederal}')

    def _checkIfNcmInList(self, ncm):
        return True if self._listNcm.count(ncm) > 0 else False

    def _makeObject(self, product):
        data_emissao = treatsFieldAsDate(self._dataXml['identificao_nfe']['data_emissao'], 2)
        return {
            "emitente_inscricao_federal": self._dataXml['emitente']['inscricao_federal'],
            "emitente_razao_social": self._dataXml['emitente']['razao_social'],
            "identificao_nfe_numero_nf": self._dataXml['identificao_nfe']['numero_nf'],
            "identificao_nfe_modelo_nf": self._dataXml['identificao_nfe']['modelo_nf'],
            "identificao_nfe_serie_nf": self._dataXml['identificao_nfe']['serie_nf'],
            "identificao_nfe_data_emissao": self._dataXml['identificao_nfe']['data_emissao'],
            "data_emissao": data_emissao,
            "month_emissao": data_emissao.month,
            "year_emissao": data_emissao.year,
            "chave_nota": self._dataXml['chave_nota'],
            "destinatario_inscricao_federal": self._dataXml['destinatario']['inscricao_federal'],
            "destinatario_razao_social": self._dataXml['destinatario']['razao_social'],
            "prod_numero_item": product['numero_item'],
            "prod_codigo_produto": product['codigo_produto'],
            "prod_nome_produto": product['nome_produto'],
            "prod_ncm": product['ncm'],
            "prod_cfop": product['cfop'],
            "prod_unidade": product['unidade'],
            "prod_quantidade": product['quantidade'],
            "prod_valor_unitario": product['valor_unitario'],
            "prod_valor_total": product['valor_total']
        }

    def _saveResult(self, dataToSave):
        self._saveData.save(
            dataToSave,
            {
                "chave_nota": dataToSave['chave_nota'],
                "prod_numero_item": dataToSave['prod_numero_item']
            }
        )

    def process(self):
        for index, product in enumerate(self._dataXml['dados_produtos']):
            product['nmc_in_list_rule'] = self._checkIfNcmInList(product['ncm'])
            dataToSave = self._makeObject(product)
            self._saveResult(dataToSave)

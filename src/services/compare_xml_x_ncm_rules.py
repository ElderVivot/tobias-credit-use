import os
import sys
from typing import Dict, List
from pymongo.database import Database

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from dao.save_data import SaveData
from utils.functions import treatsFieldAsDate, returnDataInDictOrArray


class CompareXmlXNcmRules():
    def __init__(self, database: Database, dataXml: Dict[str, dict], listNcmName: Dict[str, str], listNcm: Dict[str, str],
                 listCfopTributado: List[int], listCfopDevolucao: List[int]):
        self._database = database
        self._dataXml = dataXml
        self._listNcmName = listNcmName
        self._listNcm = listNcm
        self._listCfopTributado = listCfopTributado
        self._listCfopDevolucao = listCfopDevolucao

        inscricaoFederal = self._dataXml['emitente']['inscricao_federal']
        self._saveData = SaveData(self._database, f'notas_{inscricaoFederal}')

    def _getNcmRule(self, ncm, cfop):
        if cfop not in self._listCfopTributado:
            return 'CFOPNaoTributado'
        return returnDataInDictOrArray(self._listNcm, [ncm])

    def _getNcmName(self, ncm):
        return returnDataInDictOrArray(self._listNcmName, [ncm])

    def _amountTotalCheckDevolucaoVenda(self, amountTotal, cfop):
        if cfop in self._listCfopDevolucao and cfop < 5000:
            return amountTotal * (-1)
        return amountTotal

    def _makeObject(self, product):
        data_emissao = treatsFieldAsDate(self._dataXml['identificao_nfe']['data_emissao'], 2, getWithHour=True)
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
            "prod_name_ncm": product['name_ncm'],
            "prod_cfop": product['cfop'],
            "prod_unidade": product['unidade'],
            "prod_quantidade": product['quantidade'],
            "prod_valor_unitario": product['valor_unitario'],
            "prod_valor_produto": product['valor_produto'],
            "prod_valor_frete": product['valor_frete'],
            "prod_vseg": product['vseg'],
            "prod_valor_outros": product['valor_outros'],
            "prod_valor_desconto": product['valor_desconto'],
            "prod_valor_total": product['valor_total'],
            "prod_ncm_rule": product['nmc_rule']
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
        for product in self._dataXml['dados_produtos']:
            ncm = product['ncm']
            cfop = int(product['cfop'])
            product['nmc_rule'] = self._getNcmRule(ncm, cfop)
            product['name_ncm'] = self._getNcmName(ncm)
            product['valor_total'] = self._amountTotalCheckDevolucaoVenda(product['valor_total'], cfop)
            dataToSave = self._makeObject(product)
            self._saveResult(dataToSave)

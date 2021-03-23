import os
import sys
from typing import List
from shutil import copy

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.read_json import readJson
from utils.functions import getDateTimeNowInFormatStr
from services.compare_xml_x_ncm_rules import CompareXmlXNcmRules
from main.get_ncms_rules import GetNcms

envJson = readJson(os.path.join(dirNameSrc, '..', 'env.json'))
sys.path.append(envJson['path_library_read_nf'])

from nfe.__main__ import IndexNfe


class AnalyseNcmXml():
    def __init__(self, pathWithXmlFiles: str):
        self._pathWithXmlFiles = pathWithXmlFiles
        self._listNfeAlreadyRead: List[str] = []
        self._folderSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed',
                                              'resultado_analise', f'{getDateTimeNowInFormatStr()}.csv')

        getNcms = GetNcms(envJson['rules_of_xml'], saveResultProcessInFile=False, returnOnlyValueNcm=True, silent=True)
        self._listNcms = getNcms.processAll()

        self._writeHeader()

    def _writeHeader(self):
        with open(self._folderSaveResult, 'w') as file:
            file.write("Numero Nota;Modelo;Serie;Emissao;CNPJ Emitente;Nome Emitente;CNPJ Destinatario;Nome Destinatario;Codigo Produto;Nome Produto;NCM;CFOP;Unidade;Quantidade;Valor Unitario;Valor Total;NCM na Lista de Regra?;Chave Nota\n")

    def _process(self, pathFile):
        indexNfe = IndexNfe(pathFile)
        nfe = indexNfe.process()
        if nfe is not None:
            self._listNfeAlreadyRead.append(nfe['chave_nota'])
            if self._listNfeAlreadyRead.count(nfe['chave_nota']) > 1:
                return 'AlreadyProcessed'

            compareXmlXNcmRules = CompareXmlXNcmRules(nfe, self._listNcms, self._folderSaveResult)
            compareXmlXNcmRules.process()
        # copy files that dont read to analyse whice is problem
        else:
            copy(pathFile, os.path.join(self._pathWithXmlFiles, 'dont_read', os.path.basename(pathFile)))

    def processAll(self):
        for root, _, files in os.walk(self._pathWithXmlFiles):
            lenFiles = len(files)
            for indexFile, file in enumerate(files):
                pathFile = os.path.join(root, file)
                if file.lower().endswith(('.xml')) and pathFile.find('dont_read') < 0:
                    print(f'- Processing {pathFile} - {indexFile+1} of {lenFiles}.')
                    self._process(pathFile)


if __name__ == '__main__':
    main = AnalyseNcmXml(envJson['path_files_xml'])
    main.processAll()

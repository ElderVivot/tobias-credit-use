import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.read_json import readJson
# from services.ncms.bebidas_frias import BebidasFrias
from services.ncms.monofasicos import Monofasicos
from typing import List


class GetNcms():
    def __init__(self, saveResultProcessInFile=True, returnOnlyValueNcm=False, silent=True):
        self._saveResultProcessInFile = saveResultProcessInFile
        self._returnOnlyValueNcm = returnOnlyValueNcm
        self._silent = silent  # dont show which file is processed
        self._folderNcm = os.path.join(dirNameSrc, '..', 'data', 'ncms', 'all')
        self._folderSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed', 'ncms', 'result_process.csv')

    def _process(self, dataJson: dict) -> dict:
        # bebidasFrias = BebidasFrias(dataJson, self._returnOnlyValueNcm)
        # return bebidasFrias.cstSNVendaVarejista()

        monofasicos = Monofasicos(dataJson)
        return monofasicos.monofasicoVarejo()

    def _saveResultProcess(self, listData: List[dict]):
        with open(self._folderSaveResult, 'w') as file:
            file.write("NCM;Nome NCM;Tag Filtro;Dados da Tag\n")
            for data in listData:
                file.write(f"'{data['ncm']};{data['nameNcm']};{data['tag']};{data['dataTag']}")
                file.write('\n')

    def processAll(self) -> List[dict]:
        listData = []
        for root, _, files in os.walk(self._folderNcm):
            lenFiles = len(files)
            for indexFile, file in enumerate(files):
                if self._silent is not True:
                    print(f'- Processing {indexFile+1} of {lenFiles}.')
                if file.lower().endswith(('.json')):
                    dataJson = readJson(os.path.join(root, file))
                    resultProcess = self._process(dataJson)
                    if resultProcess is not None:
                        listData.append(resultProcess)

        if self._saveResultProcessInFile is True:
            self._saveResultProcess(listData)

        return listData


if __name__ == '__main__':
    main = GetNcms(True, False)
    print(main.processAll())

import os
import sys
from typing import List, Dict

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.read_json import readJson
from utils.functions import removeAnArrayFromWithinAnother
from services.ncms.bebidas_frias import BebidasFrias
from services.ncms.monofasicos import Monofasicos


class GetNcms():
    def __init__(self, listRules: List[str], saveResultProcessInFile=True, returnOnlyValueNcm=False, silent=True):
        self._listRules = listRules
        self._saveResultProcessInFile = saveResultProcessInFile
        self._returnOnlyValueNcm = returnOnlyValueNcm
        self._silent = silent  # dont show which file is processed
        self._folderNcm = os.path.join(dirNameSrc, '..', 'data', 'ncms', 'all')
        self._folderSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed', 'ncms', 'list_ncm_rules_filtered.csv')
        self._listNcm: Dict[str, str] = {}

    def _process(self, dataJson: dict):
        listNcm = []
        bebidasFrias = BebidasFrias(dataJson, self._returnOnlyValueNcm)
        monofasicos = Monofasicos(dataJson, self._returnOnlyValueNcm)

        for rule in self._listRules:
            dataNcm = None
            if rule == 'BebidaFria':
                dataNcm = bebidasFrias.bebidaFria()
            elif rule == 'MonofasicoVarejo':
                dataNcm = monofasicos.monofasicoVarejo()
            elif rule == 'MonofasicoAtacadoSN_CST_4':
                dataNcm = monofasicos.monofasicoAtacadoSN_CST_4()
            elif rule == 'MonofasicoAtacadoSN_CST_6':
                dataNcm = monofasicos.monofasicoAtacadoSN_CST_6()

            if dataNcm is not None:
                listNcm.append(dataNcm)
                self._listNcm[dataJson['ncm']] = rule

        return listNcm

    def _saveResultProcess(self, listData: List[dict]):
        with open(self._folderSaveResult, 'w') as file:
            file.write("NCM;Nome NCM;Tag Filtro;Dados da Tag\n")
            for data in listData:
                file.write(f"'{data['ncm']};{data['nameNcm']};{data['tag']};{data['dataTag']}")
                file.write('\n')

    def processAll(self) -> Dict[str, str]:
        listData = []
        for root, _, files in os.walk(self._folderNcm):
            lenFiles = len(files)
            for indexFile, file in enumerate(files):
                if self._silent is not True:
                    print(f'- Processing {indexFile+1} of {lenFiles}.')
                if file.lower().endswith(('.json')):
                    dataJson = readJson(os.path.join(root, file))
                    resultProcess = self._process(dataJson)
                    if resultProcess is not None and len(resultProcess) > 0:
                        listData.append(resultProcess)

        listData = removeAnArrayFromWithinAnother(listData)
        if self._saveResultProcessInFile is True:
            self._saveResultProcess(listData)

        return self._listNcm


if __name__ == '__main__':
    main = GetNcms(['MonofasicoVarejo'], saveResultProcessInFile=True,
                   returnOnlyValueNcm=False, silent=False)
    print(main.processAll())

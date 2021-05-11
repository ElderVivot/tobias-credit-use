import os
import sys
from typing import Dict, Union

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.read_json import readJson
from services.ncms.all_ncms_list import AllNcmsList


class GetNcmsName():
    def __init__(self, saveResultProcessInFile=True, silent=True):
        self._saveResultProcessInFile = saveResultProcessInFile
        self._silent = silent  # dont show which file is processed
        self._folderNcm = os.path.join(dirNameSrc, '..', 'data', 'ncms', 'all')
        self._folderSaveResult = os.path.join(dirNameSrc, '..', 'data', 'processed', 'ncms', 'list_ncms_with_name.csv')

    def _process(self, dataJson: dict) -> Union[Dict[str, str], None]:
        allNcmsList = AllNcmsList(dataJson)
        dataNcm = allNcmsList.process()
        return dataNcm

    def _saveResultProcess(self, listData: Dict[str, str]):
        with open(self._folderSaveResult, 'w') as file:
            file.write("NCM;Nome NCM\n")
            for ncm, nameNcm in listData.items():
                file.write(f"'{ncm};{nameNcm}")
                file.write('\n')

    def processAll(self):
        listData = {}
        for root, _, files in os.walk(self._folderNcm):
            lenFiles = len(files)
            for indexFile, file in enumerate(files):
                if self._silent is not True:
                    print(f'- Processing {indexFile+1} of {lenFiles}.')
                if file.lower().endswith(('.json')):
                    dataJson = readJson(os.path.join(root, file))
                    resultProcess = self._process(dataJson)
                    if resultProcess is not None:
                        listData[resultProcess['ncm']] = resultProcess['nameNcm']

        if self._saveResultProcessInFile is True:
            self._saveResultProcess(listData)

        return listData


if __name__ == '__main__':
    main = GetNcmsName(saveResultProcessInFile=True, silent=False)
    print(main.processAll())

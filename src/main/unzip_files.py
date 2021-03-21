import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from zipfile import ZipFile
from utils.functions import getOnlyNameFile


class UnzipFiles():
    def __init__(self, pathWithZipFiles: str):
        self._pathWithZipFiles = pathWithZipFiles

    def processAll(self):
        for root, _, files in os.walk(self._pathWithZipFiles):
            lenFiles = len(files)
            for indexFile, file in enumerate(files):
                pathFile = os.path.join(root, file)
                if file.lower().endswith(('.zip')):
                    print(f'- Processing {pathFile} - {indexFile} of {lenFiles}.')
                    with ZipFile(pathFile, 'r') as compressed:
                        print(compressed.namelist())
                        compressed.extractall(os.path.join(root, getOnlyNameFile(pathFile)))


if __name__ == '__main__':
    main = UnzipFiles('/home/eldervivot/Programming/microservices/read-xml-nfe/data')
    main.processAll()

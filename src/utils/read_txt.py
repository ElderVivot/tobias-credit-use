from codecs import open
import os
import sys

dirNameSrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(dirNameSrc)

from utils.functions import treatsFieldAsText


def readTxt(caminho, encoding='utf-8', treatAsText=False, removeBlankLines=False):
    lista_linha = []

    # le o arquivo e grava num vetor
    try:
        with open(caminho, 'rt') as txtfile:
            for linha in txtfile:
                linha = str(linha).replace("\n", "")
                if treatAsText is True:
                    linha = treatsFieldAsText(linha)
                if removeBlankLines is True:
                    if linha.strip() == "":
                        continue
                lista_linha.append(linha)
    except Exception:
        lista_linha.clear()
        with open(caminho, 'rt', encoding='Windows-1252') as txtfile:
            for linha in txtfile:
                linha = str(linha).replace("\n", "")
                if treatAsText is True:
                    linha = treatsFieldAsText(linha)
                if removeBlankLines is True:
                    if linha.strip() == "":
                        continue
                lista_linha.append(linha)

    return lista_linha

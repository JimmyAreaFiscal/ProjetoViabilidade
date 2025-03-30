"""

Classe para importação de Dados Abertos do CNPJ

"""
from datetime import datetime as dt 
import requests 
from bs4 import BeautifulSoup
import zipfile, requests, io
import os
import tempfile
from pathlib import Path
from parametrizacao import metadados_tabelas

class ImportadorCnpj:
    
    URL = "https://arquivos.receitafederal.gov.br/cnpj/dados_abertos_cnpj/"

    def __init__(self, mes: str):
        self.mes = mes 
        self.links = []
        self.path = "./"
        self.temp_dir = tempfile.TemporaryDirectory()
        self._coletar_links()


    def _obterHtml(self, mes: str) -> str:
        blob = requests.get(self.URL + f'/{mes}')
        return blob.text


    def _extrairLink(self, html: str) -> None:
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']

            # Quebrando o link para verificar se é Empresa, Estabelecimento ou Simples (tabelas a serem processadas)
            nome_tabela = href.split('/')[-1]
            condicao = nome_tabela.startswith('Estabelecimentos')
            if href.endswith(".zip") and condicao:
                self.links.append(self.URL + href)


    def _coletar_links(self):
        html = self._obterHtml(self.mes)
        self._extrairLink(html)
        self.links_iter = iter(self.links)


    def __iter__(self):
        return self


    def __next__(self):
        while True:
            try:
                link = next(self.links_iter)
            except StopIteration:
                self.temp_dir.cleanup()
                raise StopIteration

            ok, zip_obj = self._baixarArquivo(link)
            if not ok:
                continue

            zip_obj.extractall(self.temp_dir.name)
            arquivos_extraidos = list(Path(self.temp_dir.name).glob("*"))

            arquivos_filtrados = [
                arq for arq in arquivos_extraidos
                if any(str(arq.name).endswith(ext) for ext in metadados_tabelas)
            ]

            if arquivos_filtrados:
                return arquivos_filtrados
            else:
                continue


    def _baixarArquivo(self, link: str) -> tuple[bool, zipfile.ZipFile]:
        if not link.endswith(".zip"):
            return False, None
        
        try:
            unzpBlob = requests.get(link)
            zip = zipfile.ZipFile(io.BytesIO(unzpBlob.content), "r")
            return True, zip
        except Exception as e:
            print(f"Erro ao baixar {link}: {e}")
            return False, None

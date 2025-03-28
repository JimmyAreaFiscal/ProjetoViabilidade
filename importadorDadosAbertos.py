class importarDadosAbertos:
    def __init__(self, url):
      self.url = url
      self.links = []
      self.path = "./"


    def baixar_dados(self):
        import requests
        blob = requests.get(self.url)
        return blob.text


    def extrair_links(self, html):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a", href=True)
        self.links = [link['href'] for link in links]


    def processar(self):
        html = self.baixar_dados()
        self.extrair_links(html)
        self.unzippar(self.links)


    def unzippar(self, listalink):
        import zipfile, requests, io
        import os
        listalnk = listalink
        unzpUrl = self.url
        unzpCnt = 0
        for link in listalnk:
            try:
            
                    # Vai verificar se é um zip no link.
                    if not link.endswith(".zip"):
                        unzpCnt = unzpCnt + 1  
                        continue

                    unzpLstUrl = unzpUrl + listalnk[unzpCnt]
                    print(f"./{listalnk[unzpCnt]}")
                    unzpBlob = requests.get(unzpLstUrl)
                    unzpZip = zipfile.ZipFile(io.BytesIO(unzpBlob.content), "r")
                    unzpZip.filename
                    unzpZip.extractall(self.path)
                    unzpCnt = unzpCnt + 1   
            except zipfile.BadZipFile:
                        unzpCnt = unzpCnt + 1  
                        continue             
            
    def renomearCSV(self):
         import os
         arquivos = os.listdir(self.path)
         print(arquivos)
         for arquivo in arquivos:
              if not arquivo.endswith('.csv'):
                    os.rename(f"{self.path}/{arquivo}", f"{self.path}/{arquivo}.csv")

def main ():
    dados = importarDadosAbertos("https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2024-11/")
    dados.path = "./2024-11"
    dados.processar()
    dados.renomearCSV()

main()




















# Esse puxa um simples arquivo.

#r = requests.get("https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2024-11/Cnaes.zip")
#z = zipfile.ZipFile(io.BytesIO(r.content), "r")
#z.extractall() 
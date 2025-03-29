"""

Script para montagem de banco de dados dimensional

"""

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pathlib import Path
from data_source.parametrizacao import metadados_tabelas

class StagingCnpj:

    def __init__(self, engine: Engine):
        self.engine = engine

    def inserir_arquivo(self, arquivo: Path):
        extensao = ''.join(arquivo.name.split('.')[-2:]) if '.CSV' in arquivo.name else '.' + arquivo.suffix.upper()
        if not extensao.startswith('.'):
            extensao = '.' + extensao

        if extensao not in metadados_tabelas:
            print(f"[IGNORADO] Arquivo {arquivo.name} não reconhecido nos metadados.")
            return

        tabela_destino, colunas = metadados_tabelas[extensao]

        try:
            df = pd.read_csv(
                arquivo,
                sep=';',
                header=None,
                names=colunas,
                dtype=str,
                encoding='latin1'
            )

            df.to_sql(
                tabela_destino,
                con=self.engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=5000
            )
            print(f"[INSERIDO] {arquivo.name} na tabela '{tabela_destino}' com {len(df)} registros.")

        except Exception as e:
            print(f"[ERRO] Falha ao inserir {arquivo.name}: {e}")

    



"""

Classe para transformar os dados de CNPJ em modelagem dimensional

"""

import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text

class TransformadorDadosCnpj:

    def __init__(self, engine: Engine, mes_referencia: str):
        self.engine = engine
        self.mes_referencia = mes_referencia
        self.dados_transformados = {}

    def transformar(self) -> dict:
        # 1. Carrega os dados da staging
        estabelecimentos = pd.read_sql("SELECT * FROM Estabelecimentos", self.engine)
        empresas = pd.read_sql("SELECT * FROM Empresas", self.engine)
        simples = pd.read_sql("SELECT * FROM Simples", self.engine)

        # 2. Junta os dados
        base = (
            estabelecimentos
            .merge(empresas, on='cnpj_basico', how='left', suffixes=('', '_emp'))
            .merge(simples, on='cnpj_basico', how='left', suffixes=('', '_simples'))
        )

        # 3. Gera dimensões
        dim_tempo = pd.DataFrame([{
            'mes': self.mes_referencia[5:],
            'ano': self.mes_referencia[:4],
            'mes_referencia': self.mes_referencia
        }])

        dim_estado = (
            base[['uf']]
            .dropna()
            .drop_duplicates()
            .rename(columns={'uf': 'estado'})
            .assign(id=lambda df: range(1, len(df) + 1))
        )

        dim_cidade = (
            base[['municipio', 'uf']]
            .dropna()
            .drop_duplicates()
            .rename(columns={'municipio': 'nome_cidade', 'uf': 'estado'})
            .assign(id=lambda df: range(1, len(df) + 1))
        )

        # 4. Fato principal
        fato_empresas = base[[
            'cnpj_basico', 'capital_social_str', 'porte_empresa',
            'cnae_fiscal', 'municipio', 'uf'
        ]].copy()

        fato_empresas['capital_social'] = pd.to_numeric(
            fato_empresas['capital_social_str'].str.replace(',', '.'), errors='coerce'
        )
        fato_empresas['quantidade_empresas'] = 1
        fato_empresas['mes_referencia'] = self.mes_referencia

        # 5. Armazena resultado transformado internamente
        self.dados_transformados = {
            'DimTempo': dim_tempo,
            'DimEstado': dim_estado,
            'DimCidade': dim_cidade,
            'FatoEmpresas': fato_empresas
        }

        # 6. Limpa staging
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM Estabelecimentos"))
            conn.execute(text("DELETE FROM Empresas"))
            conn.execute(text("DELETE FROM Simples"))

        return self.dados_transformados

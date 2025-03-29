metadados_tabelas = {
        '.EMPRECSV': ("Empresa", ['cnpj_basico', 'razao_social', 'natureza_juridica', 'qualificacao_responsavel',
                                'capital_social_str', 'porte_empresa', 'ente_federativo_responsavel']),
        '.ESTABELE': ("Estabelecimento", ['cnpj_basico', 'cnpj_ordem', 'cnpj_dv', 'matriz_filial', 'nome_fantasia',
                                        'situacao_cadastral', 'data_situacao_cadastral', 'motivo_situacao_cadastral',
                                        'nome_cidade_exterior', 'pais', 'data_inicio_atividades', 'cnae_fiscal',
                                        'cnae_fiscal_secundaria', 'tipo_logradouro', 'logradouro', 'numero',
                                        'complemento', 'bairro', 'cep', 'uf', 'municipio', 'ddd1', 'telefone1', 'ddd2',
                                        'telefone2', 'ddd_fax', 'fax', 'correio_eletronico', 'situacao_especial',
                                        'data_situacao_especial']),

        '.SIMPLES.CSV': ("Simples", ['cnpj_basico', 'opcao_simples', 'data_opcao_simples', 'data_exclusao_simples',
                                   'opcao_mei', 'data_opcao_mei', 'data_exclusao_mei']),
    }

dicionario_tabelas = {
                    'EMPRECSV': "Empresas",
                    'ESTABELE': "Estabelecimentos",
                    'SOCIOCSV': "Socios",
                    'SIMPLES.CSV': "Simples", 

                    'MOTICSV': "Motivos", 
                    'MUNICCSV': "Municipios",
                    'NATJUCSV': "NaturezaJuridica",
                    'QUALSCSV': "QualificacaoSocios"
                    }
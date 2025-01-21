import numpy as np # Arrays
import pandas as pd # Tratamento de dados tabulares (planilhas)
import requests # Faz requisições ao servidor para baixar os dados
import re # Buscar padrões de texto
from zipfile import ZipFile # Abre e extrai arquivos zip
import os # Gerenciamento de arquivos e pastas
import time # Verificar o ano atual para download dos dados
from datetime import datetime, timedelta # Tratamento de datas e horas
import shutil # Deletar pastas
from warnings import filterwarnings # Silenciar mensagens irritantes :)
filterwarnings('ignore')


def download_alertario(dir_padrao):
    '''Baixa automaticamente os zips de todas as estações e anos do Alerta Rio
        Parâmetros:
            dir_padrao: None|String. Diretório onde serão criadas as pastas de download.
                        Se dir_padrao : None, cria as pastas no diretorio atual
    '''
    
    dados_brutos = os.path.join(dir_padrao,'dados_brutos')
    pasta_zip = os.path.join(dados_brutos,'zip')
    pasta_txt = os.path.join(dados_brutos,'txt')
    
    if os.path.exists(dados_brutos) == False:
        os.makedirs(dados_brutos)
    
    if os.path.exists(pasta_zip) == False:
        os.makedirs(pasta_zip)
        print('pasta zip?')
    
    if os.path.exists(pasta_txt) == False:
        os.makedirs(pasta_txt)
    
    ### Baixando os arquivos do Alerta Rio
    
    # Ano atualizado
    ano_atual = time.localtime().tm_year
    for ano in range(1997,ano_atual+1):
        # URL do endpoint
        url = 'https://websempre.rio.rj.gov.br/dados/pluviometricos/plv/'
        csrf_token = 'dkdfWVo4RKNitRkc7AI1TTX0qRrW0XE4'  # Substitua pelo token correto
        
        # Dados do formulário
        data = {
            'csrfmiddlewaretoken': csrf_token,
        }
        
        # Adiciona todas as estações e seleciona um ano específico
        for i in range(1, 34):  # 33 estações
            data[f'{i}-check'] = 'on'  # Marca todas as estações
            data[f'{i}-choice'] = str(ano)  # Seleciona o ano mais recente, por exemplo
        
        # Envia a solicitação POST
        response = requests.post(url, data=data)
        
        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Verifica o tipo de conteúdo retornado
            content_type = response.headers.get('Content-Type')
            print('Tipo de conteúdo retornado:', content_type)
        
            # Define o caminho para salvar o arquivo
            zip_file = f'DadosPluviometricos{str(ano)}.zip'
            file_path = os.path.join(pasta_zip, zip_file)
        
            # Salva o conteúdo da resposta como um arquivo se for um ZIP
            if 'application/zip' in content_type:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f'Arquivo baixado com sucesso em: {file_path}')
            else:
                print('O conteúdo retornado não é um arquivo ZIP. Verifique a resposta:')
                print(response.text)  # Imprime o conteúdo da resposta
        else:
            print('Erro ao baixar o arquivo:', response.status_code)

        # Extrai os arquivos nos zips para a pasta txt
        zips = [os.path.join(pasta_zip, arquivo_zip) for arquivo_zip in os.listdir(pasta_zip)
        if '.zip' in arquivo_zip]

        for arquivo_zip in zips:
            with ZipFile(arquivo_zip, 'r') as arquivo:
                arquivo.extractall(pasta_txt)

    # Exclui a pasta zip após o download
    shutil.rmtree(pasta_zip)
            
    return None


def apaga_desc_txt(arquivo, n_linhas = 4):
    '''Recebe um arquivo txt. Apaga até a nésima linha do arquivo (por padrão até a 4ª).
        Serve para apagar o titulo dos arquivos (Relatório  pluviométrico...)'''
    with open(arquivo,"r") as file:
        linhas = file.readlines()
        indice_linha = 1
        if 'RelatÃ³rio' in linhas[0]:
            with open(arquivo,"w") as file:
                for linha in linhas:
                    if indice_linha > n_linhas:
                        file.write(linha)
                    indice_linha += 1
    file.close()
    return None

def txt_para_csv(entrada, pasta_save = None):
    '''Converte os arquivos txt para o formato csv
        entrada: string com diretorio da pasta txt criada por DownloadAlertaRio
        pasta_save: None|string com diretorio a ser criado (ou existente) onde os
        arquivos csv serão salvos    
    '''
    
    if pasta_save == None:
        diretorio = os.path.dirname(entrada)
        pasta_save = os.path.join(diretorio, 'csv')
        
    if not os.path.exists(pasta_save):
        os.makedirs(pasta_save)

    # Caminho do arquivo de saída
    nome_csv = os.path.basename(entrada).replace('.txt', '.csv')
    saida_csv = os.path.join(pasta_save, nome_csv)
    
    # Abrir o arquivo de entrada e criar o arquivo de saída
    with open(entrada, 'r', encoding='utf-8') as txt, open(saida_csv, 'w', encoding='utf-8') as csv:
        for n_linha, linha in enumerate(txt, start = 1):
            # Corrigindo possíveis inconsistencias com as colunas que terminam com 'min' ou 'h'

            # Elementos presentes na linha ("palavras")
            valores = linha.split()
            n_elementos = len(valores)
            
            if n_linha == 1: # primeira linha (nome das colunas)
                # Lista para armazenar os nomes das colunas corrigidas
                colunas_corrigidas = []
                # indice de um elemento
                i = 0
                while i < n_elementos:
                    # Verificando se a palavra é seguida de outra palavra como 'min' ou 'h'
                    # para juntá-las em uma unica string
                    if i + 1 < n_elementos and (valores[i + 1] == 'min' or valores[i + 1] == 'h'):
                        # Junta as duas strings acrescentando ',' no final
                        colunas_corrigidas.append(f"{valores[i]} {valores[i + 1]},")
                        i += 2  # Pula o próximo elemento (ignorando a próxima palavra que deve ser 'min' ou 'h')
                    else:
                        # Se a strng não é seguida de outra string 'min' ou 'h'
                        # apenas é adicionado ',' no final
                        colunas_corrigidas.append(valores[i]+',')
                        i += 1
                # Atualizando os nomes das colunas na primeira linha pelos novos valores corrigidos  
                valores = colunas_corrigidas
                
            else:
                # Caso a coluna HBV esteja vazia, adiciona um valor 'nan'
                # A coluna HBV sempre é a 3ª (indice 2)
                if valores[2] != 'HBV':
                    valores.insert(2,'nan')

                # Substituindo todos os 'ND' por nan
                valores = ['nan' if elemento == 'ND' else elemento for elemento in valores]
                
                # Percorrendo os dados presentes na linha para adicionar ','
                # no ultimo indice
                valores = [elemento+',' for elemento in valores]

            # Colocando '\n' no ultimo elemento indicando o fim da linha
            valores[-1] = valores[-1].replace(',', '\n')
                
            linha_csv = ''.join(valores)
            csv.write(linha_csv + '\n')
    
    print(f"Arquivo convertido para CSV em: {saida_csv}\n")
    return None

def tratar_dados_faltantes(dataframe):
    '''Converte colunas do DataFrame dos CSVs, depois da coluna 'HBV', para o tipo numérico 
        e preenche os valores faltantes pela mediana das colunas

        Parâmetros:
            dataframe: pd.DataFrame
        Retorna DataFrame (DataFrame tratado)
    '''
    
    # Retirando dados faltantes substituindo pela mediana da coluna
    colunas_converter = dataframe.iloc[:,3:].columns.to_list() # colunas depois da 'HBV'
    dataframe[colunas_converter] = dataframe[colunas_converter].apply(pd.to_numeric)
    dataframe[colunas_converter] = dataframe[colunas_converter].apply(lambda x: x.fillna(x.median()))
    return dataframe

def corrigir_hbv(dataframe):
    '''Corrige as colunas de Dia e Hora cancelando os efeitos do Horário Brasileiro de Verão (HBV)
        
        Parâmetros:
           dataframe: pd.DataFrame
        Retorna DataFrame (DataFrame tratado)
    '''
    
    # Data Frame com as colunas que possuem horario de verão 
    dados_HBV = dataframe.loc[dataframe.HBV == 'HBV', ['Dia', 'Hora']].copy()
    
    if dados_HBV.empty == False: # Verifica se existe datas com horario de verão no dataframe
        # Cria uma coluna unindo a informação de data e hora no formato datetime
        dados_HBV['data_hora'] = pd.to_datetime(dados_HBV['Dia'] + ' ' + dados_HBV['Hora'], format = '%d/%m/%Y  %H:%M:%S')
        
        # Variável para retirar 1 hora dos dados
        correcao_hbv = timedelta(hours = 1)
        
        # Corrigindo o horário
        dados_HBV['data_hora'] = dados_HBV['data_hora'] - correcao_hbv
        
        # Atualizando as colunas Dia e Hora do dataframe dados_HBV
        dados_HBV['Dia'] = dados_HBV['data_hora'].apply(lambda x: x.strftime('%d/%m/%Y'))
        dados_HBV['Hora'] = dados_HBV['data_hora'].apply(lambda x: x.strftime('%H:%M:%S'))
        
        # Atribuindo ao dataframe original os valores alterados de Dia e Hora corrigidos
        dataframe.loc[dataframe.HBV == 'HBV', ['Dia', 'Hora']] = dados_HBV[['Dia', 'Hora']]
    
    # Elimina a coluna HBV
    dataframe.drop(columns = 'HBV', inplace = True)

    return dataframe

def csv_estacoes(pasta_csv,pasta_save):
    ''' Cria um DataFrame único com todas as datas para cada uma das estações
         
        Parâmetros:
           dataframe: pd.DataFrame
        Retorna DataFrame (DataFrame tratado)
    '''
    
    # Criando pasta_csv para salvar os arquivos (caso não exista)
    if os.path.exists(pasta_save) == False:
        os.makedirs(pasta_save)
    
    # Lista com os nomes dos arquivos txt presentes no diretorio
    arquivos = [csv for csv in os.listdir(pasta_csv) if '.csv' in csv]
    
    # Expressão para encontrar o padrão de texto representando o ano e mes do arquivo
    # 6 digitos (ex: 202401)
    padrao_arquivo = re.compile(r'_(\d{6})_Plv\.csv')
    
    # Separar os arquivos pela estacao, usando o trecho com a data e _Plv como separador
    # (Porque o nome da estação vem antes deste trecho!)
    # Ex: anchieta_199701_Plv -> (utilizando o trecho como separador) ['anchieta'] 
    estacoes = np.array([re.split(padrao_arquivo, csv)[0] for csv in arquivos])
    estacoes = np.unique(estacoes) #Tirando estaçoes repetidas

    # Criando progresso de loading
    loading = 0
    # estacoes
    for estacao in estacoes:
        # Criando um buscador de estacoes pelo nome
        padrao_estacao = re.compile(f'{estacao}')
        # Lista com os arquivos referentes a mesma estação
        arquivos_estacao = [os.path.join(pasta_csv, arquivo) for arquivo in arquivos if padrao_estacao.match(arquivo)]
    
        # Lista de dataframes
        df_estacao = []

        # Progresso de Loading para o tratamento e junção dos arquivos
        for arquivo in arquivos_estacao:
            # Abrindo arquivo pulando descrição em texto nas 3 primeiras linhas do arquivo
            dataframe = pd.read_csv(arquivo)
            # Tratando arquivos
            dataframe = tratar_dados_faltantes(dataframe)
            # Corrigindo horario de verão
            dataframe = corrigir_hbv(dataframe)
            # Adiciona o dataframe corrigido na lista df_estacao (Como se fosse um salvamento)
            df_estacao.append(dataframe)
        
        # Juntando todos os dataframes em um só!
        df_estacao = pd.concat(df_estacao)
        # index = False para não criar uma coluna extra com o índice
        df_estacao.to_csv(os.path.join(pasta_save, estacao + '.csv'), index = False)
        # Progresso do loading geral
        loading += 1
        print(f'Tratando e juntando dataframes : {loading*100/len(estacoes):.2f}%', end = '\r')
    return None
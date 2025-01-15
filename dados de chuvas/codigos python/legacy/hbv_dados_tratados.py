import pandas as pd
from os import listdir as ld, remove as rmv
from datetime import datetime, timedelta
import shutil

def fev_mar(arquivo):
  dados = pd.read_csv(arquivo, sep = '\t')
  fev = dados.copy()
  mar = dados.copy()

  fev.Dia = pd.to_datetime(fev.Dia, format = '%d/%m/%Y')
  mar.Dia = pd.to_datetime(fev.Dia, format = '%d/%m/%Y')

  ano_init = fev.Dia[0].year
  ano_fim = fev.Dia[fev.shape[0]-1].year

  fev_indice = []
  mar_indice = []

  while ano_init != ano_fim:
    tab_fev = fev.loc[(fev.Dia >= str(ano_init)+'-02-01') & (fev.Dia < str(ano_init)+'-03-01')]
    tab_mar = mar.loc[(mar.Dia >= str(ano_init)+'-03-01') & (mar.Dia < str(ano_init)+'-04-01')]
    list.extend(fev_indice, tab_fev.index)
    list.extend(mar_indice, tab_mar.index)
    ano_init +=1

  fev = dados.iloc[fev_indice]
  mar = dados.iloc[mar_indice]

  nome= arquivo.split('/')
  nome = nome[len(nome)-1].removesuffix('.csv')

  #salva as tabelas em arquivos
  fev.to_csv(nome+'_fev.csv', index = False, sep ='\t')
  mar.to_csv(nome+'_mar.csv', index = False, sep = '\t')

  #transforma em txt
  shutil.copy(nome+'_fev.csv', nome+'_fev.txt')
  shutil.copy(nome+'_mar.csv', nome+'_mar.txt')

  #remove os originais em csv
  rmv(nome+'_fev.csv')
  rmv(nome+'_mar.csv')


def junta_txt(diretorio, arq_espec = None):
    ''' junta_txt(       
        diretorio: str; Caminho da(s) pasta(s) que contem os arquivos txt
        arq_espec = None: None = uma pasta apenas; int indica um diretorio de pastas
        Junta os txts e os transforma em uma tabela csv. coloque no endereco o endereco da pasta regioes chuvas. '''
    
    if arq_espec != None:
        pastas = ld(diretorio)
        for pasta in pastas:
            arq = ld(diretorio+'/'+pasta)
            
            '''colspecs seleciona a região de caracteres no texto em que se encontrarão os dados (os dados da 1ª coluna 
            estarão entre o primeiro caractere da linha até o décimo) '''
            
            dados_total = pd.concat( (pd.read_fwf(diretorio+'/'+pasta+'/'+txt,
                                                  
            colspecs = [(0,10),(12,20),(22,25),(28,34),(35,41),(42,48),(49,55),(56,62)])
                                      
            for txt in arq[1:]))
            
            dados_total.to_csv("dados_total_"+pasta+".csv", index = False)
            
    else:
        arquivos = ld(diretorio)
        
        dados_total = pd.concat( (pd.read_fwf(diretorio+'/'+arq,
                                                  
        colspecs = [(0,10),(12,20),(22,25),(28,34),(35,41),(42,48),(49,55),(56,62)])
                                      
        for arq in arquivos[1:]))
​
        print(dados_total.head(25))
​
        pasta = diretorio.split("/")
​
        dados_total.to_csv("dados_total_"+pasta[len(pasta)-1]+".csv", index = False)
​
    return dados_total

def tratar(arquivo, FEV_MAR = 0, TXT = 0):

  ''' tratar(

      arquivo: string diretorio aqruivo
      FEV_MAR = 0 : int; 1 para separar fevereiro e março
      TXT = 0: int; 1 para salvar em txt

      )

      Corrige o horario de verão dos arquivos csv '''

    
    
    dados = pd.read_fwf(arquivo)
    hora = timedelta(hours=1)
    formato = "%d/%m/%Y %H:%M:%S"

    #salvando apenas os indices da tabela onde temos 'HBV' (otimiza o codigo)    
    indices_hbv = dados.loc[dados['HBV'] == 'HBV'].index 
    
    for i in indices_hbv:
        data_hbv = datetime.strptime(dados.iat[i,0]+' '+dados.iat[i,1],formato)
        correcao = data_hbv - hora
        data_corrigida = datetime.strftime(correcao,formato)
        dia, horario = data_corrigida.split()
        dados.iat[i,0] = dia
        dados.iat[i,1] = horario

    #tratando os valores das colunas

    dados.replace('ND', float(0.0), inplace = True)

    dados['HBV'].fillna(' ', inplace = True)
    dados['HBV'].replace('HBV',' ', inplace = True)
    

    #dados.drop(columns = "HBV", inplace = True) #não vamos mais precisar usar a coluna HBV já que todos os horarios estão normais
    
    nome = arquivo.split('/')

    #salvando
    dados.to_csv(nome[len(nome)-1].removesuffix('.csv')+'_corrigido.csv', index = False, sep ='\t')
    
    if FEV_MAR == 1:
      #separando em fev e mar
      fev_mar(nome[len(nome)-1].removesuffix('.csv')+'_corrigido.csv')

    if TXT == 1:
      
      #transformando em txt
      shutil.copy(nome[len(nome)-1].removesuffix('.csv')+'_corrigido.csv', nome[len(nome)-1].removesuffix('.csv')+'_corrigido.txt')
      rmv(nome[len(nome)-1].removesuffix('.csv')+'_corrigido.csv')
    
    return None

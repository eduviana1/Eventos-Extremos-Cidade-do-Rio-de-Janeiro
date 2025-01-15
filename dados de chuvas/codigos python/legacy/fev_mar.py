import pandas as pd

def fev_mar(arquivo):
  dados = pd.read_csv(arquivo)
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

  fev.to_csv(nome+'_fev.csv', index = False)
  mar.to_csv(nome+'_mar.csv', index = False)



import pandas as pd
import os
import os.path as path

def chacml(arquivo):
    if path.isfile(arquivo):
        nome = txt.replace('dados_total_','')
        nome = nome.replace('_corrigido_fev.txt','')
        fev31 = pd.read_csv(arquivo)
        fev31.Dia = pd.to_datetime(fev31.Dia, format = '%d/%m/%Y')
        fev31['ano']= fev31.Dia.dt.year
        fev31['mes'] = fev31.Dia.dt.month

        mar_indice  = fev31.loc[ fev31.mes == 3].index
        fev = fev31.drop(mar_indice)

        fev = fev[['ano','15 min']].groupby('ano').sum()
        fev.rename(columns = {'15 min': nome+' Fev'}, inplace = True)

        fev31 = fev31[['ano','15 min']].groupby('ano').sum()
        fev31.rename(columns = {'15 min': nome+' Fev31'}, inplace = True)

        total = pd.concat([fev,fev31], axis = 1)

        print(total)
        
    elif path.isdir(arquivo):
        regioes_acumul = []
        arq = os.listdir(arquivo)
        for txt in arq[1:-1]:
            nome = txt.replace('dados_total_','')
            nome = nome.replace('_corrigido_fev.txt','')
            fev31 = pd.read_csv(path.join(arquivo,txt))
            fev31.Dia = pd.to_datetime(fev31.Dia, format = '%d/%m/%Y')
            fev31['ano']= fev31.Dia.dt.year
            fev31['mes'] = fev31.Dia.dt.month

            mar_indice  = fev31.loc[ fev31.mes == 3].index
            fev = fev31.drop(mar_indice)

            fev = fev[['ano','15 min']].groupby('ano').sum()
            fev.rename(columns = {'15 min': nome+' Fev'}, inplace = True)

            fev31 = fev31[['ano','15 min']].groupby('ano').sum()
            fev31.rename(columns = {'15 min': nome+' Fev31'}, inplace = True)

            total_regiao = pd.concat([fev,fev31], axis = 1)
            list.append(regioes_acumul,total_regiao)

            #print(total_regiao)
            
        total = pd.concat(regioes_acumul,axis = 1)
        total.to_csv('total2.csv')
        print(total)
            

    return None

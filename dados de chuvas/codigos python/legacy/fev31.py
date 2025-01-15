import pandas as pd
from os import listdir as ld

def mes_ano_dia(dados,i):
    data = dados.Dia[i].split("/")
    dia = data[0]
    mes = data[1]
    ano = data[2]
    return mes,ano,dia

def fev_31(diretorio, arquivo = False):
    ano_bissexto = [2000, 2004, 2008, 2012, 2016, 2020]
    chuvas = 0
    if  arquivo == False:
        files = ld(diretorio)
        for csv in files:
            
            dados= pd.read_csv(diretorio+'/'+csv, sep = ',')
            dados['Dia'] = pd.to_datetime(dados['Dia'], format = '%d/%m/%Y')

            print(dados)

            ano_regiao = []

            chuvas = 0

            ano = dados.Dia[0].year
            ano_final = dados.Dia[(dados.shape[0])-1].year

            while ano <= ano_final:
                if ano in ano_bissexto:
                    tabela = dados.loc[ (dados['Dia'] >= str(ano)+'-02-01') & (dados['Dia'] <= str(ano)+'-03-03')]
                    chuvas += tabela['24 h'].sum()
                    list.append(ano_regiao, ano)
                    list.append(ano_regiao, chuvas)
                    ano+=1
                else:
                    tabela = dados.loc[ (dados['Dia'] >= str(ano)+'-02-01') & (dados['Dia'] <= str(ano)+'-03-02')]
                    chuvas += tabela['24 h'].sum()
                    list.append(ano_regiao, ano)
                    list.append(ano_regiao, chuvas)
                    ano+=1
            
            
            
        print(ano_regiao)

    else:
        
        dados= pd.read_csv(diretorio, sep = ',')
        dados['Dia'] = pd.to_datetime(dados['Dia'], format = '%d/%m/%Y')

        print(dados)
        
        ano_regiao = []
        
        chuvas = 0
        
        ano = dados.Dia[0].year
        ano_final = dados.Dia[(dados.shape[0])-1].year
        
        while ano <= ano_final:
            if ano in ano_bissexto:
                tabela = dados.loc[ (dados['Dia'] >= str(ano)+'-02-01') & (dados['Dia'] <= str(ano)+'-03-03')]
                chuvas += tabela['24 h'].sum()
                list.append(ano_regiao, ano)
                list.append(ano_regiao, chuvas)
                ano+=1
            else:
                tabela = dados.loc[ (dados['Dia'] >= str(ano)+'-02-01') & (dados['Dia'] <= str(ano)+'-03-02')]
                chuvas += tabela['24 h'].sum()
                list.append(ano_regiao, ano)
                list.append(ano_regiao, chuvas)
                ano+=1
        print(ano_regiao)
        
    print("final")
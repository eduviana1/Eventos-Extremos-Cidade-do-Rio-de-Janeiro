def apaga_titulo_txt(arquivo, n_linhas = 4):
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

def no_hbv(arquivo):
    
    dados = pd.read_fwf(arquivo)
    hora = timedelta(hours=1)
    formato = "%d/%m/%Y %H:%M:%S"
    
    #print(dados.loc[dados['HBV'] == 'HBV'])
    
    indices_hbv = dados.loc[dados['HBV'] == 'HBV'].index 
    
    for i in indices_hbv:
        data_hbv = datetime.strptime(dados.iat[i,0]+' '+dados.iat[i,1],formato)
        correcao = data_hbv - hora
        data_corrigida = datetime.strftime(correcao,formato)
        dia, horario = data_corrigida.split()
        dados.iat[i,0] = dia
        dados.iat[i,1] = horario

    #print(dados.loc[dados['HBV'] == 'HBV'])

    dados.replace('ND', float(0.0), inplace = True)

    dados['HBV'].fillna(' ', inplace = True)
    dados['HBV'].replace('HBV',' ', inplace = True)
    

    #dados.drop(columns = "HBV", inplace = True) #não vamos mais precisar usar a coluna HBV já que todos os horarios estão normais
    
    nome = arquivo.split('/')
    dados.to_csv(nome[len(nome)-1].removesuffix('.csv')+'_corrigido.csv', index = False)

    return None

def junta_txt(diretorio, arq_espec = None):

    '''Junta os txts e os transforma em uma tabela csv. coloque no endereco o endereco da pasta regioes chuvas'''
    if arq_espec != None:
        pastas = ld(diretorio)
        for pasta in pastas:
            arq = ld(diretorio+'/'+pasta)
            dados_total = pd.concat((pd.read_fwf(diretorio+'/'+pasta+'/'+txt , skiprows = 1, names = ['Dia','Hora','HBV','15 min','01 h','04 h', '24 h', '96 h']) for txt in arq))
            #dados_total.drop(columns = {"15", "15 min"}, inplace = True)
            #dados_total.rename(columns = {"min" : "15 min"}, inplace = True)
            #dados_total.replace("ND", 0.0, inplace = True)
            dados_total.to_csv("dados_total_"+pasta+".csv", index = False)
            
    else:
        arquivos = ld(diretorio)
            
        dados_total = pd.concat((pd.read_fwf(diretorio+'/'+arq, skiprows = 1, names = ['Dia','Hora','HBV','15 min','01 h','04 h', '24 h', '96 h']) for arq in arquivos))

        print(dados_total.head(25))

        
        #dados_total.drop(columns = {"15", "15 min"}, inplace = True)
        #dados_total.rename(columns = {"min" : "15 min"}, inplace = True)
        #dados_total.replace("ND", 0.0, inplace = True)

        pasta = diretorio.split("/")

        dados_total.to_csv("dados_total_"+pasta[len(pasta)-1]+".csv", index = False)

    return None

def corrige_hbv(diretorio):
    arquivos = ld(diretorio)
    for csv in arquivos[1:]:
        no_hbv(diretorio+'/'+csv)

    return None
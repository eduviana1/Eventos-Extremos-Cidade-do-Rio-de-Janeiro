import os
import shutil
import AlertaRioCSV

dir_padrao = os.getcwd()
# Download dos dados e criação de pastas
AlertaRioCSV.download_alertario(dir_padrao)
# Pasta onde estão baixados os arquivos txt do alerta rio
pasta_txt = os.path.join(dir_padrao,"dados_brutos/txt")

# Lista com os arquivos txt
txts = [os.path.join(pasta_txt, txt) for txt in os.listdir(pasta_txt) 
       if '.txt' in txt]

# Pasta CSV
pasta_csv = os.path.join(dir_padrao, 'dados_brutos/csv')

for txt in txts:
    # Apagando a descricao dos txts
    AlertaRioCSV.apaga_desc_txt(txt)
    # Converte os arquivos txt para csv ajustando as colunas
    AlertaRioCSV.txt_para_csv(txt, pasta_csv)

# Remove a pasta txts após a conversão para csv
shutil.rmtree(pasta_txt)

# Pasta onde serão salvos as tabelas concantenadas por estação
pasta_save = os.path.join(dir_padrao,'alerta_rio_csv')
# Criando tabelas concantendadas por estação
AlertaRioCSV.csv_estacoes(pasta_csv, pasta_save)
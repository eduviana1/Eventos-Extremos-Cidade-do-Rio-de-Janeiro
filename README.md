[requirements.txt](https://github.com/user-attachments/files/18429013/requirements.txt)# Eventos Extremos Cidade do Rio de Janeiro

## Análises de Eventos Extremos ocorridos na Cidade do Rio de Janeiro
### Descrição:

O objetivo deste projeto foi o de criar um script em Python para realizar o download e tratamento dos dados de precipitação do Sistema Alerta Rio a fim de se obter uma base de dados referentes ao período após 1997 agrupada pelas diferentes estações pluviométricas.

### Detalhes

(O Site do Alerta Rio disponibiliza os arquivos em .txt com download manual por ano e estação)
(Arquivos CSV são mais fáceis de tratar)
(Dados antigos com Horário Brasileiro de Verão) 
(Planilhas agrupadas por estação)

** Obs: A partir de Novembro de 2024 as estações pluviométricas também passaram a obter os dados de precipitação nos intervalos de 5 e 10 minutos  

AlertaRioCSV.py é um script que possui funções que são utilizadas em MainAlertaRio.py, como:

- 

### Instruções

#### O código de download dos arquivos é totalmente escrito em Python, a fim de que possa ser executado sem a necessidade de IDEs, e requer a instalação das seguintes bibliotecas:

 - numpy
 - pandas
 - requests

 Que podem ser facilmente instaladas pelo terminal com os comandos

 ```bash
 pip install numpy
 pip install pandas
 pip install requests
 ```


Caso queria utilizar o script para baixar, tratar e gerar os CSVs, execute o MainAlertaRio.py que deve estar no mesmo diretório que o script AlertaRioCSV.py



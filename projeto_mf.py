import pandas as pd
import requests 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import os


ticker = input("digit o ticker: ")
url = f"https://finance.yahoo.com/quote/{ticker}.SA/history/?period1=1590516222&period2=1748282618"
table_att = ['Data', 'Abertura', 'Máxima', 'Mínima', 'Fechamento', 'Volume']


def extract(url, table_att):
    """
    Função para extrair a tabela com as informações
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36"
    }
    
    html_page = requests.get(url, headers=headers).text
    data = BeautifulSoup(html_page, "html.parser")
    df = pd.DataFrame(columns=table_att)

    table = data.find_all('tbody')
    rows = table[0].find_all('tr')

    for row in rows:
        column = row.find_all('td')
        if len(column) == 7: # no site cada linha da table tem exatamente 7 colunas
            date_text = column[0].text.strip()
            try:
                # Tentar converter a data para garantir que é uma data válida
                datetime.strptime(date_text, '%b %d, %Y')
            except ValueError:
                # Se não for data válida, pula a linha
                continue
            data_dict = {'Data': column[0].text.strip(), 'Abertura': column[1].text.strip(), 'Máxima': column[2].text.strip()
                        , 'Mínima': column[3].text.strip(), 'Fechamento': column[4].text.strip(), 'Volume': column[6].text.strip()}
            df2 = pd.DataFrame(data_dict, index = [0])
            df = pd.concat([df, df2], ignore_index=True)
            df['Data'] = pd.to_datetime(df['Data'], format='%b %d, %Y', errors='coerce')

    
    print("Dados extraidos com sucesso!")
    return df
    

df = extract(url, table_att)


def transform(df):
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
    for col in ['Abertura', 'Máxima', 'Mínima', 'Fechamento']:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '').str.strip()  # Remove vírgulas e espaços
            df[col] = pd.to_numeric(df[col], errors='coerce')   # Converte para float, valores inválidos viram NaN
        else:
            df[col] = df[col].astype(float)

    
    # Tratar o Volume
    df['Volume'] = df['Volume'].replace('-', np.nan)
    if df['Volume'].dtype == 'object':
        df['Volume'] = df['Volume'].str.replace(',', '')
        df['Volume'] = df['Volume'].fillna('0').astype(int)
    else:
        df['Volume'] = df['Volume'].astype(int)

    # Médias móveis exponenciais
    df['Ema_10'] = df['Fechamento'].ewm(span=10, adjust=False).mean()
    df['Ema_50'] = df['Fechamento'].ewm(span=50, adjust=False).mean()
    df['Ema_200'] = df['Fechamento'].ewm(span=200, adjust=False).mean()

    print("Dados transformados com sucesso!")
    return df


df = transform(df)


data_max = df['Data'].max()
data_min = data_max - pd.DateOffset(years=5)
df_plot = df[(df['Data'] >= data_min) & (df['Data'] <= data_max)]


plt.figure(figsize=(14,7))

plt.plot(df_plot['Data'], df_plot['Fechamento'], label='Fechamento', color='blue')
plt.plot(df_plot['Data'], df_plot['Ema_10'], label='EMA 10', color='red')
plt.plot(df_plot['Data'], df_plot['Ema_50'], label='EMA 50', color='green')
plt.plot(df_plot['Data'], df_plot['Ema_200'], label='EMA 200', color='orange')

plt.title('Preço Fechamento e Médias Móveis Exponenciais (EMA)')
plt.xlabel('Data')
plt.ylabel('Preço (R$)')
plt.legend()
plt.grid(True)

# Ajuste do eixo X para mostrar datas legíveis
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # a cada 3 meses
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gcf().autofmt_xdate()  # rotaciona datas

plt.savefig(f'Dados_Historicos_{ticker}.png', dpi=300, bbox_inches='tight')


def salvar(df, ticker):
    filename = f"{ticker}_dados.csv"  # nome do arquivo com o ticker
    df.to_csv(filename, index=False)  # salva sem o índice
    print(f"Arquivo salvo como {filename}, na pasta: ", os.getcwd())


salvar(df, ticker)
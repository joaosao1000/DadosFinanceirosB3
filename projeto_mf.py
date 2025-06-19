import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

ticker = input("Digite o ticker: ")
url = f"https://finance.yahoo.com/quote/{ticker}.SA/history/?period1=1590516222&period2=1748282618"
table_att = ['Data', 'Abertura', 'Máxima', 'Mínima', 'Fechamento', 'Volume']

def extract(url, table_att):
    """
    Função para extrair a tabela com Selenium (renderiza JavaScript)
    """
    # Configurações do Chrome em modo headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicializar driver
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # Espera o JavaScript carregar a tabela

    # Pega o HTML renderizado
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    df = pd.DataFrame(columns=table_att)
    table = soup.find("table")

    if not table:
        print("Tabela não encontrada. Verifique o ticker.")
        return df

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [td.text.strip() for td in cols]
        if len(cols) == 7:
            try:
                datetime.strptime(cols[0], '%b %d, %Y')
                data_dict = {
                    'Data': cols[0],
                    'Abertura': cols[1],
                    'Máxima': cols[2],
                    'Mínima': cols[3],
                    'Fechamento': cols[4],
                    'Volume': cols[6]
                }
                df2 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df, df2], ignore_index=True)
            except:
                continue

    df['Data'] = pd.to_datetime(df['Data'], format='%b %d, %Y', errors='coerce')
    print("Dados extraídos com sucesso!")
    return df

df = extract(url, table_att)

def transform(df):
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    for col in ['Abertura', 'Máxima', 'Mínima', 'Fechamento']:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            df[col] = df[col].astype(float)

    df['Volume'] = df['Volume'].replace('-', np.nan)
    if df['Volume'].dtype == 'object':
        df['Volume'] = df['Volume'].str.replace(',', '')
        df['Volume'] = df['Volume'].fillna('0').astype(int)
    else:
        df['Volume'] = df['Volume'].astype(int)

    df['Ema_10'] = df['Fechamento'].ewm(span=10, adjust=False).mean()
    df['Ema_50'] = df['Fechamento'].ewm(span=50, adjust=False).mean()
    df['Ema_200'] = df['Fechamento'].ewm(span=200, adjust=False).mean()
    print("Dados transformados com sucesso!")
    return df

df = transform(df)

data_max = df['Data'].max()
data_min = data_max - pd.DateOffset(years=5)
df_plot = df[(df['Data'] >= data_min) & (df['Data'] <= data_max)]

plt.figure(figsize=(14, 7))
plt.plot(df_plot['Data'], df_plot['Fechamento'], label='Fechamento', color='blue')
plt.plot(df_plot['Data'], df_plot['Ema_10'], label='EMA 10', color='red')
plt.plot(df_plot['Data'], df_plot['Ema_50'], label='EMA 50', color='green')
plt.plot(df_plot['Data'], df_plot['Ema_200'], label='EMA 200', color='orange')

plt.title('Preço Fechamento e Médias Móveis Exponenciais (EMA)')
plt.xlabel('Data')
plt.ylabel('Preço (R$)')
plt.legend()
plt.grid(True)

plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gcf().autofmt_xdate()

plt.savefig(f'Dados_Historicos_{ticker}.png', dpi=300, bbox_inches='tight')

def salvar(df, ticker):
    filename = f"{ticker}_dados.csv"
    df.to_csv(filename, index=False)
    print(f"Arquivo salvo como {filename}, na pasta: {os.getcwd()}")

salvar(df, ticker)

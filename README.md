# Analise de ações na B3 dos últimos 5 anos

Projeto para extração, limpeza, análise e visualização de dados históricos da bolsa brasileira (B3) utilizando dados do Yahoo Finance.

## Objetivo

- Extrair dados históricos de ações da B3 via web scraping.
- Limpar e transformar os dados para análise.
- Calcular indicadores financeiros como Médias Móveis Exponenciais (EMA).
- Visualizar dados e indicadores para facilitar tomada de decisão.
- Salvar dados em CSV e gráficos em imagens para uso futuro.
- Preparar dados para possível uso em bancos de dados na nuvem (ex.: Azure).

## Tecnologias

- Python 3  
- Bibliotecas: pandas, requests, BeautifulSoup, matplotlib  
- Ambiente: Jupyter Notebook / VS Code

## Funcionalidades

- Extração automatizada de dados históricos para um certo ticker inserido pelo usuário.  
- Tratamento e limpeza dos dados (conversão de tipos, remoção de valores inválidos).  
- Cálculo de indicadores técnicos financeiros.  
- Geração de gráficos com os preços e indicadores.  
- Exportação dos dados tratados para CSV e gráficos para PNG.

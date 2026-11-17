# Análise de ações da B3

Pipeline em Python que extrai cotações históricas de ações da B3, trata os
dados, calcula indicadores técnicos e gera as visualizações.

## O que faz

Você informa o ticker, e o pipeline:

1. Extrai o histórico de cotações
2. Trata os dados — conversão de tipos, remoção de registros inválidos,
   tratamento de pregões sem negociação
3. Calcula médias móveis exponenciais
4. Gera o gráfico de preço com os indicadores sobrepostos
5. Exporta a série tratada em CSV e o gráfico em PNG

## Como rodar

```bash
git clone https://github.com/joaosao1000/<repo>.git
cd <repo>
pip install -r requirements.txt
python main.py
```

Digite o ticker quando solicitado (ex.: `PETR4.SA`).

## Decisões de projeto

**Por que scraping com Selenium.** [PREENCHER — ver observação abaixo]

**Tratamento de dias sem pregão.** Feriado e fim de semana não geram registro,
então a série não é contínua em dias corridos. O cálculo das EMAs usa a
sequência de pregões, não o calendário.

## O que eu faria diferente hoje

- Trocar o scraping por uma biblioteca de dados de mercado — menos frágil a
  mudança de layout e muito mais rápido
- Adicionar cache local pra não reextrair a mesma série a cada execução
- Permitir comparação entre múltiplos tickers na mesma execução
- Cobrir o cálculo dos indicadores com testes

## Stack

`Python 3` · `pandas` · `Selenium` · `requests` · `matplotlib`

# brasil-macro-credito

Projeto pessoal em Python para coletar, analisar e visualizar indicadores
macroeconômicos brasileiros — Selic, IPCA, câmbio (USD/BRL) e inadimplência
de crédito de pessoas físicas — a partir da API pública do Banco Central
(SGS).

A ideia surgiu como projeto de portfólio ao me candidatar a um estágio na
Nubank: quis unir meu interesse por macroeconomia e mercados emergentes a
uma pergunta bem concreta do mundo de crédito/fintech — **como juros,
inflação e câmbio se relacionam com a inadimplência das famílias?**

## O que o projeto faz

1. **Coleta** quatro séries temporais direto da API do Banco Central
   (SGS - Sistema Gerenciador de Séries Temporais):
   - Meta Selic (% a.a.)
   - IPCA — variação mensal (%)
   - Dólar comercial (USD/BRL)
   - Inadimplência da carteira de crédito — Pessoas Físicas (%)
2. **Organiza** tudo em uma única série mensal com pandas.
3. **Analisa** a correlação de cada variável com a inadimplência e monta
   um índice simples de "pressão sobre o crédito" (média de z-scores de
   Selic, IPCA e câmbio).
4. **Gera gráficos** (matplotlib) com a evolução de cada indicador e do
   índice.

## Como rodar

```bash
git clone <url-do-seu-repositorio>
cd brasil-macro-credito
pip install -r requirements.txt
python main.py
```

Isso baixa os dados mais recentes direto da API do BCB, imprime um resumo
estatístico e as correlações no terminal, e salva:

- `dados_macro_brasil.csv` — dados brutos usados na análise
- `graficos_macro.png` — evolução de cada indicador
- `indice_pressao_credito.png` — evolução do índice sintético

> É necessário acesso à internet para consultar a API do Banco Central
> (`api.bcb.gov.br`).

## Estrutura

```
brasil-macro-credito/
├── fetch_data.py   # coleta das séries via API do BCB (SGS)
├── analysis.py     # correlações e índice de pressão sobre o crédito
├── main.py         # orquestra tudo e gera os gráficos
├── requirements.txt
└── README.md
```

## Próximos passos

- Adicionar mais variáveis (desemprego, massa salarial, PIB) para
  enriquecer a análise.
- Testar um modelo preditivo simples (regressão) para a inadimplência
  usando as variáveis macro como features.
- Automatizar a atualização periódica dos dados (ex.: GitHub Actions).

## Fonte dos dados

Todos os dados vêm do [Sistema Gerenciador de Séries Temporais (SGS) do
Banco Central do Brasil](https://dadosabertos.bcb.gov.br/), uma API
pública e gratuita.

"""
fetch_data.py

Coleta séries temporais macroeconômicas do Brasil via API pública do
Banco Central (SGS - Sistema Gerenciador de Séries Temporais).

Documentação oficial: https://dadosabertos.bcb.gov.br/
"""

import pandas as pd
import requests

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

# Códigos das séries no SGS (verificados em dadosabertos.bcb.gov.br)
SERIES = {
    "selic": 432,                # Meta Selic definida pelo Copom (% a.a.)
    "ipca": 433,                 # IPCA - variação mensal (%)
    "usd_brl": 1,                # Dólar comercial - venda (diário)
    "inadimplencia_pf": 21084,   # Inadimplência da carteira de crédito - PF - Total (%)
}


def fetch_series(codigo: int, data_inicial: str, data_final: str) -> pd.DataFrame:
    """
    Busca uma série temporal do SGS/BCB entre duas datas.

    Parâmetros
    ----------
    codigo : int
        Código da série no SGS.
    data_inicial, data_final : str
        Datas no formato 'dd/mm/aaaa'.

    Retorna
    -------
    pd.DataFrame com colunas ['data', 'valor'].
    """
    url = BASE_URL.format(codigo=codigo)
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()

    df = pd.DataFrame(resp.json())
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df


def fetch_all(data_inicial: str = "01/01/2015", data_final: str | None = None) -> pd.DataFrame:
    """
    Busca todas as séries definidas em SERIES e as combina em um único
    DataFrame mensal (média do mês), indexado por data.
    """
    if data_final is None:
        data_final = pd.Timestamp.today().strftime("%d/%m/%Y")

    colunas = {}
    for nome, codigo in SERIES.items():
        serie = fetch_series(codigo, data_inicial, data_final)
        colunas[nome] = serie.set_index("data")["valor"]

    df = pd.concat(colunas.values(), axis=1)
    df.columns = list(colunas.keys())
    df = df.sort_index()

    # USD/BRL é diário; as demais já são mensais. Reamostra tudo para
    # frequência mensal usando a média do período.
    df_mensal = df.resample("MS").mean()
    return df_mensal


if __name__ == "__main__":
    dados = fetch_all()
    print(dados.tail())
    dados.to_csv("dados_macro_brasil.csv")
    print("\nDados salvos em dados_macro_brasil.csv")

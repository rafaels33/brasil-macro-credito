"""
analysis.py

Funções de análise sobre os dados macroeconômicos coletados:
- correlação entre juros/inflação/câmbio e inadimplência
- índice sintético de "pressão sobre o crédito"
"""

import pandas as pd


def calcular_correlacoes(df: pd.DataFrame, alvo: str = "inadimplencia_pf") -> pd.Series:
    """
    Calcula a correlação de cada variável macro com a série-alvo
    (por padrão, a inadimplência de pessoas físicas).
    """
    corrs = df.drop(columns=[alvo]).corrwith(df[alvo])
    return corrs.sort_values(ascending=False)


def indice_pressao_credito(df: pd.DataFrame) -> pd.Series:
    """
    Cria um índice simples (média de z-scores) de "pressão sobre o crédito",
    combinando Selic, IPCA e câmbio normalizados.

    Quanto maior o índice, maior a pressão macroeconômica sobre a
    capacidade de pagamento das famílias. É uma proxy didática para fins
    de portfólio, não um modelo de risco de crédito real.
    """
    variaveis = ["selic", "ipca", "usd_brl"]
    z = (df[variaveis] - df[variaveis].mean()) / df[variaveis].std()
    indice = z.mean(axis=1)
    return indice.rename("indice_pressao_credito")


def resumo_estatistico(df: pd.DataFrame) -> pd.DataFrame:
    """Estatísticas descritivas básicas de cada série."""
    return df.describe().T

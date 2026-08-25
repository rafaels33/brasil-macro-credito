"""
main.py

Ponto de entrada do projeto: coleta os dados do Banco Central, roda as
análises e gera os gráficos e o CSV de saída.

Uso:
    python main.py
"""

import matplotlib.pyplot as plt

from analysis import calcular_correlacoes, indice_pressao_credito, resumo_estatistico
from fetch_data import fetch_all

ROXO_NU = "#8A05BE"


def plot_series(df, out_path="graficos_macro.png"):
    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(df.index, df["selic"], color=ROXO_NU)
    axes[0].set_title("Selic (% a.a.)")

    axes[1].plot(df.index, df["ipca"], color=ROXO_NU)
    axes[1].set_title("IPCA - variação mensal (%)")

    axes[2].plot(df.index, df["usd_brl"], color=ROXO_NU)
    axes[2].set_title("USD/BRL")

    axes[3].plot(df.index, df["inadimplencia_pf"], color=ROXO_NU)
    axes[3].set_title("Inadimplência PF - Total (%)")

    plt.xlabel("Data")
    fig.suptitle("Indicadores macroeconômicos do Brasil", fontsize=14)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"Gráfico salvo em {out_path}")


def plot_indice(indice, out_path="indice_pressao_credito.png"):
    plt.figure(figsize=(10, 4))
    plt.plot(indice.index, indice.values, color=ROXO_NU)
    plt.axhline(0, color="gray", linestyle="--", linewidth=1)
    plt.title("Índice de pressão sobre o crédito (proxy)")
    plt.xlabel("Data")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"Gráfico salvo em {out_path}")


def main():
    print("Coletando dados do Banco Central (SGS)...")
    df = fetch_all(data_inicial="01/01/2017")
    df = df.dropna()    

    print("\nResumo estatístico:")
    print(resumo_estatistico(df))

    print("\nCorrelação com inadimplência PF:")
    print(calcular_correlacoes(df))

    indice = indice_pressao_credito(df)

    plot_series(df)
    plot_indice(indice)

    df.to_csv("dados_macro_brasil.csv")
    print("\nDados brutos salvos em dados_macro_brasil.csv")


if __name__ == "__main__":
    main()

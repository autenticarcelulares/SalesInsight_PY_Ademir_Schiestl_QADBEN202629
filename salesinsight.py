### SCTec
##  SalesInsight_PY_Ademir_Schiestl_QADBEN202629
##  SalesInsight PY — análise e visualização de dados de vendas.

"""Meu projeto de análise e visualização de dados de vendas com Python."""

from __future__ import annotations
import json, random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Any
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "vendas.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "graficos"
MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


# RF01 — Gero a base de vendas quando o arquivo CSV não está disponível.
def gerar_dataset_vendas(n_registros: int = 200, seed: int = 42) -> pd.DataFrame:
    """Gero vendas fictícias e incluo algumas datas inválidas para demonstrar a limpeza."""
    random.seed(seed)
    np.random.seed(seed)
    produtos = [
        "Notebook",
        "Smartphone",
        "Tablet",
        "Monitor",
        "Teclado",
        "Mouse",
        "Headset",
    ]
    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Perifericos",
        "Mouse": "Perifericos",
        "Headset": "Perifericos",
    }
    precos = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
        "Headset": 350,
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    inicio = datetime(2025, 1, 1)
    linhas = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        data = (inicio + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        if random.random() < 0.03:
            data = "DATA INVALIDA"
        linhas.append(
            {
                "id_venda": i + 1,
                "data_venda": data,
                "cliente": f"Cliente_{random.randint(1,50):03d}",
                "produto": produto,
                "categoria": categorias[produto],
                "regiao": random.choice(regioes),
                "quantidade": random.randint(1, 10),
                "preco_unitario": round(
                    precos[produto] * random.uniform(0.85, 1.15), 2
                ),
            }
        )
    return pd.DataFrame(linhas)


# RF02 — Verifico o formato, as colunas, os tipos, os valores nulos e os primeiros registros.
def inspecionar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Examino a estrutura dos dados antes de começar o tratamento."""
    print("\\n=== INSPEÇÃO INICIAL ===")
    print("Shape:", df.shape, "\\nColunas:", list(df.columns))
    print(
        "\\nTipos:\\n",
        df.dtypes,
        "\\nNulos:\\n",
        df.isnull().sum(),
        "\\nPrimeiros registros:\\n",
        df.head(),
    )
    return df


# RF03 — Trato os textos, converto datas e números e apresento o relatório de limpeza.
def tratar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Padronizo os textos e removo as linhas com datas ou números que não consigo converter."""
    d = df.copy()
    entrada = len(d)
    for c in d.select_dtypes(include=["object", "string"]).columns:
        d[c] = d[c].astype("string").str.strip()
    datas = pd.to_datetime(d["data_venda"], errors="coerce")
    invalidas = int(datas.isna().sum())
    d["data_venda"] = datas
    qtd_ant = d["quantidade"].copy()
    qtd = pd.to_numeric(d["quantidade"], errors="coerce")
    qtd_conv = int((qtd_ant.notna() & qtd.notna()).sum())
    qtd_invalidas = int(qtd.isna().sum())
    d["quantidade"] = qtd
    preco_ant = d["preco_unitario"].copy()
    preco = pd.to_numeric(d["preco_unitario"], errors="coerce")
    preco_conv = int((preco_ant.notna() & preco.notna()).sum())
    preco_invalidos = int(preco.isna().sum())
    d["preco_unitario"] = preco
    d = d.dropna(subset=["data_venda", "quantidade", "preco_unitario"])
    d["quantidade"] = d["quantidade"].astype(int)
    d["preco_unitario"] = d["preco_unitario"].astype(float)
    rel = {
        "registros_entrada": entrada,
        "datas_convertidas": int(datas.notna().sum()),
        "datas_invalidas_removidas": invalidas,
        "quantidades_convertidas": qtd_conv,
        "quantidades_invalidas": qtd_invalidas,
        "precos_convertidos": preco_conv,
        "precos_invalidos": preco_invalidos,
        "registros_finais": len(d),
        "registros_removidos_total": entrada - len(d),
    }
    print("\\n=== RELATÓRIO DE LIMPEZA ===")
    for k, v in rel.items():
        print(f"{k}: {v}")
    return d.reset_index(drop=True), rel


# RF04 — Acrescento a receita, o mês, o trimestre, o ano e as faixas de valor.
def criar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Calculo a receita de cada venda e crio as colunas que vou usar na análise."""
    d = df.copy()
    d["receita_total"] = d["quantidade"] * d["preco_unitario"]
    d["mes"] = d["data_venda"].dt.month
    d["mes_nome"] = d["mes"].map(MESES)
    d["trimestre"] = "Q" + d["data_venda"].dt.quarter.astype(str)
    d["ano"] = d["data_venda"].dt.year
    cond = [
        d.receita_total < 500,
        (d.receita_total >= 500) & (d.receita_total < 5000),
        d.receita_total >= 5000,
    ]
    for c, n in zip(cond, ["Baixo Valor", "Médio Valor", "Alto Valor"]):
        if "faixa_receita_item" not in d:
            d["faixa_receita_item"] = "Não Classificado"
        d.loc[c, "faixa_receita_item"] = n
    return d


# RF05 — Uso groupby para analisar as vendas por mês, produto, categoria e região.
def calcular_metricas(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Agrupo as vendas para comparar os resultados de cada período e grupo."""
    m = (
        df.groupby(["ano", "mes", "mes_nome", "trimestre"], as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            quantidade=("quantidade", "sum"),
            n_vendas=("id_venda", "count"),
        )
        .sort_values(["ano", "mes"])
    )
    p = (
        df.groupby("produto", as_index=False)
        .receita_total.sum()
        .sort_values("receita_total", ascending=False)
        .head(5)
    )
    c = (
        df.groupby("categoria", as_index=False)
        .receita_total.sum()
        .sort_values("receita_total", ascending=False)
    )
    r = (
        df.groupby("regiao", as_index=False)
        .agg(
            receita_total=("receita_total", "sum"),
            ticket_medio=("receita_total", "mean"),
            n_vendas=("id_venda", "count"),
        )
        .sort_values("receita_total", ascending=False)
    )
    result = {"por_mes": m, "top_produtos": p, "por_categoria": c, "por_regiao": r}
    for nome, tabela in result.items():
        print(f"\\n=== {nome.upper()} ===\\n", tabela.to_string(index=False))
    return result


# RF06 — Classifico os clientes em Bronze, Prata e Ouro usando lambda.
def segmentar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """Somo o gasto de cada cliente e uso esse total para definir seu segmento."""
    c = (
        df.groupby("cliente", as_index=False)
        .receita_total.sum()
        .rename(columns={"receita_total": "total_gasto"})
    )
    c["segmento"] = c.total_gasto.apply(
        lambda x: "Bronze" if x < 5000 else ("Prata" if x <= 15000 else "Ouro")
    )
    c = c.sort_values("total_gasto", ascending=False)
    print("\\n=== 10 MAIORES CLIENTES ===\\n", c.head(10).to_string(index=False))
    print("\\n=== CLIENTES POR SEGMENTO ===\\n", c.segmento.value_counts().to_string())
    return c


# RF08 — Reutilizo funções e passo uma função como argumento para transformar uma coluna.
def processar_coluna(
    df: pd.DataFrame,
    coluna: str,
    funcao_transformacao: Callable[[Any], Any],
    nome_saida: str | None = None,
) -> pd.DataFrame:
    """Aplico à coluna a função de transformação que recebo como argumento."""
    d = df.copy()
    d[nome_saida or f"{coluna}_transformado"] = d[coluna].apply(funcao_transformacao)
    return d


# RF07 — Crio gráficos de linha, barras, dispersão e um painel 2×2 e salvo em PNG.
def gerar_graficos(df: pd.DataFrame, metricas: dict[str, pd.DataFrame]) -> list[Path]:
    """Apresento os resultados nos quatro gráficos solicitados na atividade."""
    CHARTS.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    pal = {"Computadores": "#2457A6", "Celulares": "#E07A2D", "Perifericos": "#27856A"}
    m, p, r = metricas["por_mes"], metricas["top_produtos"], metricas["por_regiao"]
    paths = []
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        m.mes_nome,
        m.receita_total,
        color="#2457A6",
        marker="o",
        lw=2.5,
        label="Receita",
    )
    ax.set(title="Receita total por mês", xlabel="Mês", ylabel="Receita (R$)")
    ax.tick_params(axis="x", rotation=35)
    ax.legend()
    fig.tight_layout()
    f = CHARTS / "receita_por_mes.png"
    fig.savefig(f, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(f)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=p,
        y="produto",
        x="receita_total",
        hue="produto",
        legend=False,
        palette=["#2457A6", "#E07A2D", "#27856A", "#7656A5", "#C84C4C"][: len(p)],
        ax=ax,
    )
    ax.set(title="Top 5 produtos por receita", xlabel="Receita (R$)", ylabel="Produto")
    fig.tight_layout()
    f = CHARTS / "top_produtos.png"
    fig.savefig(f, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(f)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="quantidade",
        y="receita_total",
        hue="categoria",
        palette=pal,
        s=70,
        alpha=0.8,
        ax=ax,
    )
    ax.set(
        title="Quantidade vendida × receita por transação",
        xlabel="Quantidade",
        ylabel="Receita (R$)",
    )
    ax.legend(title="Categoria")
    fig.tight_layout()
    f = CHARTS / "quantidade_vs_receita.png"
    fig.savefig(f, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(f)

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    axs[0, 0].plot(
        m.mes_nome, m.receita_total, color="#2457A6", marker="o", label="Receita"
    )
    axs[0, 0].set(title="Receita por mês", xlabel="Mês", ylabel="Receita (R$)")
    axs[0, 0].tick_params(axis="x", rotation=35)
    axs[0, 0].legend()
    axs[0, 1].barh(p.produto, p.receita_total, color="#E07A2D")
    axs[0, 1].set(title="Top produtos", xlabel="Receita (R$)", ylabel="Produto")
    for cat, cor in pal.items():
        parte = df[df.categoria == cat]
        axs[1, 0].scatter(
            parte.quantidade, parte.receita_total, label=cat, color=cor, alpha=0.75
        )
    axs[1, 0].set(
        title="Quantidade × receita", xlabel="Quantidade", ylabel="Receita (R$)"
    )
    axs[1, 0].legend(title="Categoria", fontsize=8)
    axs[1, 1].bar(r.regiao, r.receita_total, color="#27856A")
    axs[1, 1].set(title="Receita por região", xlabel="Região", ylabel="Receita (R$)")
    axs[1, 1].tick_params(axis="x", rotation=25)
    fig.suptitle("SalesInsight PY — Painel Resumo", fontsize=16, weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    f = CHARTS / "painel_resumo.png"
    fig.savefig(f, dpi=150, bbox_inches="tight")
    plt.close(fig)
    paths.append(f)
    print(
        "\\nGráficos exportados:",
        *[str(x.relative_to(ROOT)) for x in paths],
        sep="\\n- ",
    )
    return paths


# RF09 — Salvo os resultados em CSV e JSON e releio o JSON para conferir a gravação.
def exportar_resultados(
    metricas: dict[str, pd.DataFrame],
    clientes: pd.DataFrame,
    estatisticas: dict[str, Any],
) -> dict[str, Path]:
    """Exporto as tabelas e as estatísticas e confiro o conteúdo do JSON gravado."""
    OUT.mkdir(parents=True, exist_ok=True)
    a = OUT / "metricas_por_mes.csv"
    b = OUT / "segmentacao_clientes.csv"
    c = OUT / "estatisticas_gerais.json"
    metricas["por_mes"].to_csv(a, index=False, encoding="utf-8-sig")
    clientes.to_csv(b, index=False, encoding="utf-8-sig")
    serial = {
        k: round(float(v), 2) if isinstance(v, (int, float, np.number)) else v
        for k, v in estatisticas.items()
    }
    with c.open("w", encoding="utf-8") as arq:
        json.dump(serial, arq, indent=4, ensure_ascii=False)
    with c.open("r", encoding="utf-8") as arq:
        print("\\nJSON gravado e relido:", json.load(arq))
    return {"metricas_por_mes": a, "segmentacao_clientes": b, "estatisticas_gerais": c}


# Organizo o fluxo nesta classe e reutilizo as funções dos requisitos RF01 a RF09.
class AnalisadorDeVendas:
    """Reúno as etapas da análise e guardo os dados e resultados entre elas."""

    def __init__(self):
        self.df_bruto = None
        self.df = None
        self.relatorio_limpeza = {}
        self.metricas = {}
        self.clientes = None
        self.graficos = []

    # RF01 — Carrego a base de vendas a partir do arquivo CSV.
    def carregar(self, caminho):
        """Leio o CSV e guardo os dados originais antes das transformações."""
        self.df_bruto = pd.read_csv(caminho)
        return self.df_bruto

    def transformar(self):
        """Trato os dados, crio novas colunas e aplico as transformações com lambda."""
        if self.df_bruto is None:
            raise ValueError("Carregue os dados primeiro.")
        limpo, self.relatorio_limpeza = tratar_dados(self.df_bruto)
        self.df = criar_colunas_derivadas(limpo)
        self.df = processar_coluna(
            self.df,
            "receita_total",
            lambda x: round(x / 1000, 2),
            "receita_em_milhares",
        )
        self.df = processar_coluna(
            self.df,
            "quantidade",
            lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
            "perfil_volume",
        )
        return self.df

    def analisar(self):
        """Calculo as métricas e classifico os clientes pelo gasto acumulado."""
        if self.df is None:
            raise ValueError("Transforme os dados primeiro.")
        self.metricas = calcular_metricas(self.df)
        self.clientes = segmentar_clientes(self.df)
        return self.metricas

    def visualizar(self):
        """Gero os quatro gráficos a partir dos dados e das métricas calculadas."""
        if self.df is None or not self.metricas:
            raise ValueError("Analise os dados primeiro.")
        self.graficos = gerar_graficos(self.df, self.metricas)
        return self.graficos

    def resumo(self):
        """Calculo os totais da análise, exporto os resultados e mostro o resumo."""
        if self.df is None or self.clientes is None:
            raise ValueError("Analise os dados primeiro.")
        stats = {
            "registros_analisados": len(self.df),
            "clientes_unicos": self.df.cliente.nunique(),
            "receita_total": self.df.receita_total.sum(),
            "quantidade_total_vendida": self.df.quantidade.sum(),
            "ticket_medio": self.df.receita_total.mean(),
            "produtos_distintos": self.df.produto.nunique(),
        }
        exportar_resultados(self.metricas, self.clientes, stats)
        print(
            "\\n=== ESTATÍSTICAS GERAIS ===\\n",
            json.dumps(stats, indent=4, ensure_ascii=False, default=float),
        )
        return stats


# RF10 — Executo todas as etapas: leitura, tratamento, análise e exportação.
def main():
    """Organizo aqui a sequência completa de execução do meu projeto."""
    print("=" * 60 + "\\n SALESINSIGHT PY — ANÁLISE DE DADOS DE VENDAS\\n" + "=" * 60)
    if not CSV.exists():
        gerar_dataset_vendas().to_csv(CSV, index=False)
    a = AnalisadorDeVendas()
    a.carregar(CSV)
    inspecionar_dados(a.df_bruto)
    a.transformar()
    a.analisar()
    a.visualizar()
    a.resumo()
    print("\\n[CONCLUÍDO] Fluxo finalizado com sucesso.")


# RF10 — Inicio a análise quando executo este arquivo diretamente.
if __name__ == "__main__":
    main()

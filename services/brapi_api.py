import os
import requests

API_TOKEN = os.getenv("API_TOKEN_BRAPI")


def get_dados_acao(ticker: str):
    """
    Busca dados detalhados de uma ação, incluindo cotação, dados fundamentalistas
    e perfis da empresa.
    """
    modules = "summaryProfile,defaultKeyStatistics"
    url = f"https://brapi.dev/api/quote/{ticker}?range=1y&interval=1mo&fundamental=true&modules={modules}"
    if API_TOKEN:
        url += f"&token={API_TOKEN}"

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(
            f"Erro ao buscar dados da Brapi para {ticker}: {response.status_code} - {response.text}"
        )

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError(f"Ticker '{ticker}' não encontrado na Brapi ou sem dados.")

    acao = results[0]

    # Coleta os dados básicos
    dados_acao = {
        "ticker": acao.get("symbol"),
        "nome": acao.get("longName") or acao.get("shortName"),
        "preco": acao.get("regularMarketPrice"),
        "historico": acao.get("historicalDataPrice"),
        "lpa": acao.get("eps"),  # LPA de 'fundamental=true'
        "p_vpa": acao.get("priceToBook"),
        "dividend_yield": acao.get("dividendYield"),
        "summaryProfile": acao.get("summaryProfile"),
        "defaultKeyStatistics": acao.get("defaultKeyStatistics"),
    }

    # Tenta usar um LPA mais completo do 'defaultKeyStatistics' se disponível
    if dados_acao.get("defaultKeyStatistics") and dados_acao["defaultKeyStatistics"].get(
        "trailingEps"
    ):
        dados_acao["lpa"] = dados_acao["defaultKeyStatistics"]["trailingEps"]

    return dados_acao
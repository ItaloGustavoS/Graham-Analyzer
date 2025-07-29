import requests


def get_dados_acao(ticker: str):
    url = f"https://brapi.dev/api/quote/{ticker}?fundamental=true&range=1y&interval=1mo"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(
            f"Erro ao buscar dados da Brapi para {ticker}: {response.status_code}"
        )

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise ValueError("Ticker não encontrado na Brapi.")

    acao = results[0]

    return {
        "ticker": acao.get("symbol"),
        "preco": acao.get("regularMarketPrice"),
        "lpa": acao.get("eps"),
        "p_vpa": acao.get("priceToBook"),
        "dividend_yield": acao.get("dividendYield"),
        "historico": acao.get("historicalDataPrice"),
        "nome": acao.get("shortName"),
    }

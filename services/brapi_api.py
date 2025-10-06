import os
import requests
import streamlit as st
import logging

API_TOKEN = os.getenv("API_TOKEN_BRAPI")

@st.cache_data(ttl=600)  # Cache por 10 minutos
def get_dados_acao(ticker: str):
    """
    Busca dados detalhados de uma ação, incluindo cotação, dados fundamentalistas
    e perfis da empresa.
    """
    modules = "summaryProfile,defaultKeyStatistics"
    url = f"https://brapi.dev/api/quote/{ticker}?range=1y&interval=1mo&fundamental=true&modules={modules}"
    if API_TOKEN:
        url += f"&token={API_TOKEN}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)

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

    except requests.RequestException as e:
        logging.error(f"Erro na requisição à API Brapi para o ticker {ticker}: {e}")
        raise ValueError("Não foi possível buscar os dados da ação no momento. Verifique o ticker e tente novamente mais tarde.")
    except (KeyError, IndexError, ValueError) as e:
        logging.error(f"Erro ao processar os dados da API para o ticker {ticker}: {e}")
        raise ValueError(f"Os dados recebidos para o ticker '{ticker}' são inválidos ou incompletos.")
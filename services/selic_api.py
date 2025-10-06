import requests
import streamlit as st

@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_selic_atual():
    url = (
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    )
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("Erro ao obter taxa Selic.")

    dados = response.json()[0]
    selic = float(dados["valor"].replace(",", "."))
    return round(selic, 2)

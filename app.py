import streamlit as st
from datetime import datetime
import pandas as pd

from services.brapi_api import get_dados_acao
from services.selic_api import get_selic_atual
from utils.validators import validar_ticker
from utils.app_helpers import (
    display_profile,
    display_main_metrics,
    display_key_stats,
    render_graham_analysis,
    plot_history,
    export_csv,
    handle_pdf_generation,
    display_saved_data,
)

# --- Page Configuration ---
st.set_page_config(page_title="Financial Dashboard B3", layout="wide")
st.title("📊 Financial Dashboard para Ativos da B3")

# --- Main Application Logic ---
def run_dashboard():
    """Main function to run the financial asset dashboard."""
    ticker = st.text_input(
        "Digite o ticker do ativo (ex: PETR4, MXRF11)", ""
    ).upper().strip()

    if not ticker:
        return

    if not validar_ticker(ticker):
        st.warning("⚠️ Ticker inválido. Digite somente letras e números.")
        return

    try:
        with st.spinner("🔎 Buscando dados..."):
            dados = get_dados_acao(ticker)
            selic = get_selic_atual()

        st.header(
            f"Análise de: {dados.get('nome', ticker)} ({dados.get('ticker', ticker)})"
        )

        # --- Display Dashboard ---
        display_profile(dados.get("summaryProfile"))
        display_main_metrics(dados)
        display_key_stats(dados.get("defaultKeyStatistics"))

        fig = plot_history(dados.get("historico"))

        # --- Conditional Graham Analysis ---
        lpa = dados.get("lpa")
        if lpa is not None and lpa > 0:
            st.markdown("---")
            g = st.number_input(
                "Taxa de crescimento estimada dos lucros para a análise de Graham (%)",
                value=5.0,
                min_value=-50.0,
                max_value=50.0,
                step=0.1,
                key="graham_growth_rate",
            )
            render_graham_analysis(lpa, g, selic, dados["preco"])
        else:
            st.info("Análise de Graham não disponível (LPA não informado ou não positivo).")

        # --- PDF Report Generation ---
        if st.button("📄 Gerar Relatório PDF"):
            key_stats = dados.get("defaultKeyStatistics", {})
            dados_para_pdf = {
                "Ticker": dados.get("ticker", "N/A"),
                "Nome": dados.get("nome", "N/A"),
                "Preço Atual": f"R$ {dados.get('preco', 0.0):.2f}",
                "P/L": f"{key_stats.get('trailingPE', 'N/A'):.2f}"
                if isinstance(key_stats.get("trailingPE"), (int, float))
                else "N/A",
                "P/VPA": f"{dados.get('p_vpa', 0.0):.2f}" if dados.get("p_vpa") else "N/A",
                "Dividend Yield": f"{dados.get('dividend_yield', 0.0) * 100:.2f}%"
                if dados.get("dividend_yield")
                else "N/A",
            }
            handle_pdf_generation(dados_para_pdf, fig)

        display_saved_data()

    except ValueError as ve:
        st.error(f"❌ Erro de Validação: {ve}")
    except Exception as e:
        st.error(f"❌ Erro Inesperado: {e}")


if __name__ == "__main__":
    run_dashboard()

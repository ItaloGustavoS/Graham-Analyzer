from datetime import datetime
import pandas as pd
import streamlit as st

from services.brapi_api import get_dados_acao
from services.selic_api import get_selic_atual
from utils.graham import calcular_valor_intrinseco
from utils.validators import validar_ticker
from utils.app_helpers import (
    render_metrics,
    plot_history,
    export_csv,
    handle_pdf_generation,
    display_saved_data,
)

# --- Page Configuration ---
st.set_page_config(page_title="Graham Analyzer B3", layout="centered")
st.title("📊 Graham Analyzer para Ações da B3")

# --- Main Application Logic ---
def run_analysis():
    """Main function to run the stock analysis."""
    ticker = st.text_input("Digite o ticker da ação (ex: PETR4)", "").upper().strip()

    if not ticker:
        return

    if not validar_ticker(ticker):
        st.warning("⚠️ Ticker inválido. Digite somente letras e números.")
        return

    try:
        with st.spinner("🔎 Buscando dados..."):
            dados = get_dados_acao(ticker)
            selic = get_selic_atual()

        lpa = dados.get("lpa")
        nome_acao = dados.get("nome", ticker)
        st.subheader(f"📈 Análise de: {nome_acao} ({dados.get('ticker', ticker)})")

        if lpa is None:
            st.error(f"❌ LPA não disponível para {ticker}.")
            return

        g = st.number_input(
            "Taxa de crescimento estimada dos lucros (%)",
            value=6.0,
            min_value=-50.0,
            max_value=50.0,
            step=0.1,
        )

        valor_intrinseco = calcular_valor_intrinseco(lpa, g, selic)
        preco_atual = dados["preco"]
        margem = round((valor_intrinseco - preco_atual) / preco_atual * 100, 2)

        # --- Display Results ---
        render_metrics(dados, valor_intrinseco, margem, selic)

        fig = plot_history(dados.get("historico"))

        # --- Data Export ---
        df_output = pd.DataFrame(
            [
                {
                    "Data": datetime.today().strftime("%Y-%m-%d"),
                    "Ticker": dados["ticker"],
                    "Nome": nome_acao,
                    "LPA": lpa,
                    "Crescimento (%)": g,
                    "Taxa Selic (%)": selic,
                    "Valor Intrínseco": valor_intrinseco,
                    "Preço Atual": preco_atual,
                    "Margem (%)": margem,
                    "P/VPA": dados["p_vpa"],
                    "Dividend Yield": dados["dividend_yield"],
                }
            ]
        )
        export_csv(df_output)

        # --- PDF Report Generation ---
        if st.button("📄 Gerar Relatório PDF"):
            dados_para_pdf = {
                "Data": datetime.today().strftime("%d/%m/%Y"),
                "Ticker": dados["ticker"],
                "Nome": nome_acao,
                "LPA": f"R$ {lpa}",
                "Taxa de Crescimento": f"{g}%",
                "Taxa Selic": f"{selic}%",
                "Valor Intrínseco": f"R$ {valor_intrinseco}",
                "Preço Atual": f"R$ {preco_atual}",
                "Margem de Segurança": f"{margem}%",
                "P/VPA": dados["p_vpa"],
                "Dividend Yield": f"{dados['dividend_yield']}%",
            }
            handle_pdf_generation(dados_para_pdf, fig)

        display_saved_data()

    except ValueError as ve:
        st.error(f"❌ Erro de Validação: {ve}")
    except Exception as e:
        st.error(f"❌ Erro Inesperado: Ocorreu um erro ao processar a solicitação: {e}")

if __name__ == "__main__":
    run_analysis()
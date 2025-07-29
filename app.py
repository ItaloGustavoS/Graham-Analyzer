from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

from services.brapi_api import get_dados_acao
from services.selic_api import get_selic_atual
from utils.graham import calcular_valor_intrinseco
from utils.validators import validar_ticker

# Configuração da página
st.set_page_config(page_title="Graham Analyzer B3", layout="centered")
st.title("📊 Graham Analyzer para Ações da B3")

# Input do ticker
ticker = st.text_input("Digite o ticker da ação (ex: PETR4)", "").upper().strip()

if ticker:
    if not validar_ticker(ticker):
        st.warning("⚠️ Ticker inválido. Digite somente letras e números.")
    else:
        try:
            with st.spinner("🔎 Buscando dados..."):
                dados = get_dados_acao(ticker)
                selic = get_selic_atual()

                lpa = dados["lpa"]
                g = st.number_input(
                    "Taxa de crescimento estimada dos lucros (%)",
                    value=6.0,
                    min_value=0.0,
                    max_value=50.0,
                    step=0.1,
                )

                valor_intrinseco = calcular_valor_intrinseco(lpa, g, selic)
                preco_atual = dados["preco"]
                nome_acao = dados["nome"]
                margem = round((valor_intrinseco - preco_atual) / preco_atual * 100, 2)

                # Exibição
                st.subheader(f"📈 Análise de: {nome_acao} ({dados['ticker']})")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("💰 Preço atual", f"R$ {preco_atual}")
                    st.metric("📊 LPA", f"R$ {lpa}")
                    st.metric("📉 Taxa Selic", f"{selic}%")

                with col2:
                    st.metric("🧮 Valor Intrínseco", f"R$ {valor_intrinseco}")
                    st.metric(
                        "📐 Margem de Segurança", f"{margen}%", delta=f"{margen}%"
                    )
                    st.metric("🏦 P/VPA", f"{dados['p_vpa']}")
                    st.metric("💵 Dividend Yield", f"{dados['dividend_yield']}%")

                # Gráfico de preço histórico
                st.markdown("### 📅 Histórico de Preço (últimos 12 meses)")
                historico = dados["historico"]

                if historico:
                    df_hist = pd.DataFrame(historico)
                    df_hist["date"] = pd.to_datetime(df_hist["date"])
                    df_hist = df_hist.sort_values(by="date")
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=df_hist["date"],
                            y=df_hist["close"],
                            mode="lines+markers",
                            name="Preço de Fechamento",
                        )
                    )
                    fig.update_layout(
                        title="Histórico de Preço",
                        xaxis_title="Data",
                        yaxis_title="Preço (R$)",
                        template="plotly_white",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("⚠️ Sem dados históricos disponíveis.")

                # Exportar para CSV
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
                            "Margem (%)": margen,
                            "P/VPA": dados["p_vpa"],
                            "Dividend Yield": dados["dividend_yield"],
                        }
                    ]
                )

                try:
                    df_output.to_csv(
                        "data/historico_consultas.csv",
                        mode="a",
                        header=False,
                        index=False,
                    )
                except FileNotFoundError:
                    df_output.to_csv(
                        "data/historico_consultas.csv", mode="w", index=False
                    )

                with st.expander("📁 Ver dados salvos"):
                    historico_csv = pd.read_csv("data/historico_consultas.csv")
                    st.dataframe(historico_csv)

        except Exception as e:
            st.error(f"❌ Erro: {e}")

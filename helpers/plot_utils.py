import pandas as pd
import plotly.graph_objs as go
import streamlit as st

def plot_history(historico):
    """Plot the historical price data."""
    if not historico:
        st.info("⚠️ Sem dados históricos disponíveis.")
        return None

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
        title="Histórico de Preço (Últimos 12 Meses)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)
    return fig
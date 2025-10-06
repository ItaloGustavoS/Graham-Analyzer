import os
import time
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from utils.pdf_report import gerar_relatorio_pdf


def format_value(value):
    """Format large numbers into a human-readable format (M, B, T)."""
    if value is None or not isinstance(value, (int, float)):
        return "N/A"
    if abs(value) >= 1e12:
        return f"{value / 1e12:.2f} T"
    if abs(value) >= 1e9:
        return f"{value / 1e9:.2f} B"
    if abs(value) >= 1e6:
        return f"{value / 1e6:.2f} M"
    return f"{value:.2f}"


def display_profile(profile):
    """Display the company's summary profile."""
    if not profile:
        st.warning("Perfil da empresa não disponível.")
        return

    st.subheader("Perfil da Empresa")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Setor:** {profile.get('sector', 'N/A')}")
    with col2:
        st.info(f"**Indústria:** {profile.get('industry', 'N/A')}")

    with st.expander("Ver Descrição da Empresa"):
        st.markdown(f"_{profile.get('longBusinessSummary', 'N/A')}_")


def display_main_metrics(dados):
    """Display the main price and dividend metrics."""
    st.subheader("Principais Métricas")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Preço Atual", f"R$ {dados.get('preco', 0.0):.2f}")
    col2.metric("📈 Variação (Dia)", f"{dados.get('change', 0.0):.2f}%")
    col3.metric("📊 Volume", format_value(dados.get('volume')))
    col4.metric("💵 Dividend Yield", f"{dados.get('dividend_yield', 0.0) * 100:.2f}%" if dados.get('dividend_yield') else "N/A")


def display_key_stats(stats):
    """Display key financial statistics."""
    if not stats:
        st.warning("Estatísticas fundamentalistas não disponíveis.")
        return

    st.subheader("Estatísticas Chave (Últimos 12 Meses)")
    col1, col2, col3 = st.columns(3)

    # Dictionary to map keys to more readable labels
    key_map = {
        "marketCap": "Valor de Mercado",
        "enterpriseValue": "Valor da Firma",
        "trailingPE": "P/L",
        "priceToBook": "P/VPA",
        "enterpriseToRevenue": "EV/Receita",
        "enterpriseToEbitda": "EV/EBITDA",
        "trailingEps": "LPA",
        "roe": "ROE",
        "roa": "ROA",
        "debtToEquity": "Dívida/Capital",
        "netDebt": "Dívida Líquida",
        "totalRevenue": "Receita Total",
    }

    metrics = {label: format_value(stats.get(key)) for key, label in key_map.items()}

    # Display metrics in columns
    metrics_list = list(metrics.items())
    cols = [col1, col2, col3]
    for i, (label, value) in enumerate(metrics_list):
        cols[i % 3].metric(label, value)


def render_graham_analysis(lpa, g, selic, preco_atual):
    """Render the Graham Intrinsic Value analysis section."""
    from utils.graham import calcular_valor_intrinseco

    st.subheader("Análise de Valor Intrínseco (Graham)")

    valor_intrinseco = calcular_valor_intrinseco(lpa, g, selic)
    margem = round((valor_intrinseco - preco_atual) / preco_atual * 100, 2)

    col1, col2 = st.columns(2)
    col1.metric("🧮 Valor Intrínseco (Estimado)", f"R$ {valor_intrinseco:.2f}")
    col2.metric("📐 Margem de Segurança", f"{margem:.2f}%", delta=f"{margem:.2f}%")


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


def export_csv(df_output, path="data/historico_consultas.csv"):
    """Export the analysis data to a CSV file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df_output.to_csv(path, mode="a", header=not os.path.exists(path), index=False)
    except Exception as e:
        st.error(f"Erro ao salvar o arquivo CSV: {e}")


def handle_pdf_generation(dados_para_pdf, fig, tmp_dir="temp"):
    """Generate and provide a download link for the PDF report."""
    os.makedirs(tmp_dir, exist_ok=True)
    chart_path = None
    timestamp = int(time.time())

    if fig:
        chart_path = os.path.join(
            tmp_dir, f"chart_{dados_para_pdf['Ticker']}_{timestamp}.png"
        )
        fig.write_image(chart_path)

    pdf_filename = f"Relatorio_{dados_para_pdf['Ticker']}_{timestamp}.pdf"
    pdf_path = os.path.join(tmp_dir, pdf_filename)

    gerar_relatorio_pdf(
        dados=dados_para_pdf, chart_image_path=chart_path, output_path=pdf_path
    )

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=f.read(),
            file_name=pdf_filename,
            mime="application/pdf",
        )


def display_saved_data(path="data/historico_consultas.csv"):
    """Display the saved consultation history in an expander."""
    with st.expander("📁 Ver dados salvos"):
        try:
            historico_csv = pd.read_csv(path)
            st.dataframe(historico_csv)
        except FileNotFoundError:
            st.info("Nenhum histórico de consulta encontrado.")
        except pd.errors.ParserError:
            st.error("Erro ao ler o arquivo de histórico: formato inválido.")
        except Exception as e:
            st.error(f"Erro inesperado ao ler o histórico: {e}")
import os
import time
import pandas as pd
import plotly.graph_objs as go
import streamlit as st

from utils.pdf_report import gerar_relatorio_pdf


def render_metrics(dados, valor_intrinseco, margem, selic):
    """Render the financial metrics in two columns."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Preço atual", f"R$ {dados['preco']}")
        st.metric("📊 LPA", f"R$ {dados['lpa']}")
        st.metric("📉 Taxa Selic", f"{selic}%")
    with col2:
        st.metric("🧮 Valor Intrínseco", f"R$ {valor_intrinseco}")
        st.metric("📐 Margem de Segurança", f"{margem}%", delta=f"{margem}%")
        st.metric("🏦 P/VPA", f"{dados['p_vpa']}")
        st.metric("💵 Dividend Yield", f"{dados['dividend_yield']}%")


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
        title="Histórico de Preço",
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
    """
    Generate and provide a download link for the PDF report.
    The generated files are not cleaned up immediately to prevent race conditions.
    """
    os.makedirs(tmp_dir, exist_ok=True)
    chart_path = None
    timestamp = int(time.time())

    # If a figure is available, save it to a temporary file with a unique name.
    if fig:
        chart_path = os.path.join(
            tmp_dir, f"chart_{dados_para_pdf['Ticker']}_{timestamp}.png"
        )
        fig.write_image(chart_path)

    # Generate a unique PDF name and path.
    pdf_filename = f"Relatorio_{dados_para_pdf['Ticker']}_{timestamp}.pdf"
    pdf_path = os.path.join(tmp_dir, pdf_filename)

    # Generate the PDF, which can handle a None chart_path.
    gerar_relatorio_pdf(
        dados=dados_para_pdf, chart_image_path=chart_path, output_path=pdf_path
    )

    # Provide the download button.
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
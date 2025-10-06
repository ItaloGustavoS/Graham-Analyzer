import os
import time
import streamlit as st
import pandas as pd
from utils.pdf_report import gerar_relatorio_pdf

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
    Temporary files are cleaned up after the download button is created.
    """
    os.makedirs(tmp_dir, exist_ok=True)
    chart_path = None
    pdf_path = None
    timestamp = int(time.time())

    try:
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
    finally:
        # Clean up temporary files after a short delay
        time.sleep(1)
        if chart_path and os.path.exists(chart_path):
            try:
                os.remove(chart_path)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário do gráfico: {e}")
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário do PDF: {e}")

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
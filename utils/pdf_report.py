import os
from fpdf import FPDF

class GrahamPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(
            0, 10, "Relatório de Valuation - Graham Analyzer B3", ln=True, align="C"
        )
        self.ln(10)

def add_analysis(self, dados: dict, chart_image_path: str = None):
    self.set_font("Helvetica", "", 12)
    for chave, valor in dados.items():
        self.cell(0, 10, f"{chave}: {valor}", ln=True)
    self.ln(5)

    if chart_image_path and os.path.exists(chart_image_path):
        self.image(chart_image_path, x=10, y=None, w=190)

def gerar_relatorio_pdf(
    dados: dict,
    chart_image_path: str = None,
    output_path: str = "relatorio_graham.pdf",
):
    pdf = GrahamPDF()
    pdf.add_page()
    pdf.add_analysis(dados, chart_image_path)
    pdf.output(output_path)
    return output_path

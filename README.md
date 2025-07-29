# 📊 Graham Analyzer B3

Aplicativo desenvolvido em Python com Streamlit para calcular o valor intrínseco de ações da B3 utilizando a fórmula modificada de **Benjamin Graham**.

Os dados são obtidos de APIs públicas (Brapi e Banco Central), e os resultados são salvos em CSV local. Ideal para investidores que seguem a filosofia de **Value Investing**.

---

## ✅ Funcionalidades

- Busca de dados fundamentalistas via [Brapi.dev](https://brapi.dev/)
- Recuperação automática da **taxa Selic** atual
- Aplicação da fórmula de Benjamin Graham:

  \[
  \text{Valor Intrínseco} = \frac{LPA \times (8{,}5 + 2g) \times 4{,}4}{\text{Taxa Selic}}
  \]

- Gráfico do histórico de preços (12 meses)
- Indicadores:
  - LPA
  - P/VPA
  - Dividend Yield
  - Margem de segurança (%)
- Armazenamento dos resultados em CSV
- Visualização do histórico de análises
- Interface amigável com Streamlit

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/graham-analyzer-b3.git
cd graham-analyzer-b3
```

# 📊 Graham Analyzer B3

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)

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

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável:

```
API_TOKEN_BRAPI="SEU_TOKEN_AQUI"
```

Substitua `"SEU_TOKEN_AQUI"` pelo seu token da [Brapi.dev](https://brapi.dev/).

### 5. Execute o aplicativo

```bash
streamlit run app.py
```

---

## ☁️ Deploy no Streamlit Cloud

Para fazer o deploy deste aplicativo no Streamlit Cloud, siga estes passos:

1. **Faça o fork deste repositório** para a sua conta do GitHub.
2. **Acesse o [Streamlit Cloud](https://share.streamlit.io/)** e clique em "New app".
3. **Selecione o repositório** que você acabou de criar.
4. **Configure as variáveis de ambiente** (Secrets) no menu "Advanced settings...":
   - `API_TOKEN_BRAPI`: Cole o seu token da Brapi.dev aqui.
5. **Clique em "Deploy!"** e aguarde a finalização do processo.

O aplicativo estará disponível no link gerado pelo Streamlit Cloud.

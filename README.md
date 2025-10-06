# 📊 Financial Dashboard B3

[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)

Um dashboard financeiro completo, desenvolvido em Python com Streamlit, para análise de ativos da B3 (Ações, FIIs, BDRs, ETFs).

Este aplicativo busca dados detalhados de ativos através da API da [Brapi.dev](https://brapi.dev/), fornecendo uma visão consolidada de cotações, indicadores fundamentalistas, perfil da empresa e histórico de preços.

---

## ✅ Funcionalidades

- **Dashboard Detalhado**: Visualize informações consolidadas sobre qualquer ativo listado na B3.
- **Perfil da Empresa**: Acesso rápido ao setor, indústria e descrição do negócio da empresa.
- **Métricas de Mercado**: Acompanhe o preço atual, variação diária, volume de negociação e Dividend Yield.
- **Estatísticas Fundamentalistas**: Análise de múltiplos e indicadores chave como P/L, P/VPA, ROE, ROA, Dívida Líquida, e mais.
- **Gráfico Histórico**: Visualize o comportamento do preço do ativo nos últimos 12 meses.
- **Análise de Graham (Condicional)**: Para ativos com Lucro Por Ação (LPA) positivo, o dashboard oferece uma análise de valor intrínseco baseada na fórmula de Benjamin Graham.
- **Exportação para PDF**: Gere um relatório em PDF com os principais dados da análise.
- **Histórico de Consultas**: Suas análises são salvas localmente em um arquivo CSV para referência futura.

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/financial-dashboard-b3.git
cd financial-dashboard-b3
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

Crie um arquivo `.env` na raiz do projeto e adicione a seguinte variável (opcional, mas recomendado para mais requisições):

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
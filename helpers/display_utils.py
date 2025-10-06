import streamlit as st
from utils.graham import calcular_valor_intrinseco

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

    # Create a grid layout with 3 columns
    cols = st.columns(3)

    # Iterate through the metrics and display them in the grid
    for i, (key, label) in enumerate(key_map.items()):
        value = stats.get(key)
        formatted_value = format_value(value)
        cols[i % 3].metric(label, formatted_value)


def render_graham_analysis(lpa, g, selic, preco_atual):
    """Render the Graham Intrinsic Value analysis section."""
    st.subheader("Análise de Valor Intrínseco (Graham)")

    valor_intrinseco = calcular_valor_intrinseco(lpa, g, selic)
    margem = round((valor_intrinseco - preco_atual) / preco_atual * 100, 2)

    col1, col2 = st.columns(2)
    col1.metric("🧮 Valor Intrínseco (Estimado)", f"R$ {valor_intrinseco:.2f}")
    col2.metric("📐 Margem de Segurança", f"{margem:.2f}%", delta=f"{margem:.2f}%")
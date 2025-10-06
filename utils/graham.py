def calcular_valor_intrinseco(lpa: float, g: float, selic: float) -> float:
    """
    Calcula o valor intrínseco de uma ação usando a fórmula modificada de Benjamin Graham.
    """
    if selic == 0:
        return 0.0

    try:
        growth_rate = g
        # Se a taxa de crescimento `g` for um decimal, converte para porcentagem
        if abs(g) < 1:
            growth_rate = g * 100

        valor_intrinseco = (lpa * (8.5 + 2 * growth_rate) * 4.4) / selic
        return round(valor_intrinseco, 2)
    except Exception as e:
        raise ValueError(f"Erro ao calcular valor intrínseco: {e}") from e

def validar_ticker(ticker: str) -> bool:
    """
    Verifica se o ticker é válido (apenas letras e números).
    """
    return ticker.isalnum() and len(ticker) >= 4

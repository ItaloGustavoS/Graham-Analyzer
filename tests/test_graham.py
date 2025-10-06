import pytest
from utils.graham import calcular_valor_intrinseco

def test_calcular_valor_intrinseco_lpa_nulo():
    """Test that a ValueError is raised when LPA is None."""
    with pytest.raises(ValueError, match="LPA não pode ser nulo."):
        calcular_valor_intrinseco(lpa=None, g=5.0, selic=10.0)

def test_calcular_valor_intrinseco_selic_zero():
    """Test that the function returns 0 when SELIC is zero to avoid division by zero."""
    assert calcular_valor_intrinseco(lpa=1.0, g=5.0, selic=0) == 0.0

def test_calcular_valor_intrinseco_calculo_correto():
    """Test the intrinsic value calculation with standard positive inputs."""
    lpa = 2.5
    g = 7.0
    selic = 11.0
    # Formula: (lpa * (8.5 + 2 * g) * 4.4) / selic
    # (2.5 * (8.5 + 2 * 7.0) * 4.4) / 11.0 = 22.5
    expected_value = 22.5
    assert calcular_valor_intrinseco(lpa, g, selic) == expected_value

def test_calcular_valor_intrinseco_crescimento_negativo():
    """Test the calculation with a negative growth rate."""
    lpa = 3.0
    g = -2.0
    selic = 10.0
    # (3.0 * (8.5 + 2 * -2.0) * 4.4) / 10.0 = 5.94
    expected_value = 5.94
    assert calcular_valor_intrinseco(lpa, g, selic) == expected_value

def test_calcular_valor_intrinseco_crescimento_decimal():
    """Test the calculation with a decimal growth rate."""
    lpa = 1.8
    g = 0.05  # Represents 5%
    selic = 9.0
    # growth_rate is converted to 5.0 inside the function
    # (1.8 * (8.5 + 2 * 5.0) * 4.4) / 9.0 = 16.28
    expected_value = 16.28
    assert calcular_valor_intrinseco(lpa, g, selic) == expected_value

def test_calcular_valor_intrinseco_lpa_zero():
    """Test the calculation when LPA is zero."""
    assert calcular_valor_intrinseco(lpa=0, g=10.0, selic=10.0) == 0.0
import sys
import os
import pytest

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.graham import calcular_valor_intrinseco

def test_calcular_valor_intrinseco_lpa_nulo():
    with pytest.raises(ValueError, match="LPA não pode ser nulo."):
        calcular_valor_intrinseco(lpa=None, g=5.0, selic=10.0)

def test_calcular_valor_intrinseco_selic_zero():
    assert calcular_valor_intrinseco(lpa=1.0, g=5.0, selic=0) == 0.0

def test_calcular_valor_intrinseco_calculo_correto():
    lpa = 2.5
    g = 7.0
    selic = 11.0
    # (2.5 * (8.5 + 2 * 7.0) * 4.4) / 11.0 = 22.5
    expected_value = 22.5
    assert calcular_valor_intrinseco(lpa, g, selic) == expected_value
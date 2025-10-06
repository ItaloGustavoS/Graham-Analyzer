import unittest
from utils.graham import calcular_valor_intrinseco

class TestGrahamFormula(unittest.TestCase):
    def test_valor_intrinseco_padrao(self):
        # LPA = 5.0, crescimento = 6%, Selic = 10%
        valor = calcular_valor_intrinseco(5.0, 6.0, 10.0)
        self.assertAlmostEqual(valor, 45.1, places=1)

    def test_valor_intrinseco_zero_crescimento(self):
        valor = calcular_valor_intrinseco(10.0, 0.0, 11.0)
        self.assertAlmostEqual(valor, 34.0, places=1)

    def test_valor_intrinseco_selic_zero(self):
        valor = calcular_valor_intrinseco(10.0, 5.0, 0.0)
        self.assertEqual(valor, 0.0)

    def test_valor_intrinseco_com_g_decimal(self):
        # Teste com taxa de crescimento em decimal
        valor = calcular_valor_intrinseco(lpa=5.0, g=0.06, selic=10.0)
        self.assertAlmostEqual(valor, 45.1, places=1)

    def test_valor_intrinseco_com_g_negativo(self):
        # Teste com taxa de crescimento negativa
        valor = calcular_valor_intrinseco(lpa=5.0, g=-5.0, selic=10.0)
        self.assertAlmostEqual(valor, -3.3, places=1)

    def test_valor_intrinseco_com_g_negativo_decimal(self):
        # Teste com taxa de crescimento negativa em decimal
        valor = calcular_valor_intrinseco(lpa=5.0, g=-0.05, selic=10.0)
        self.assertAlmostEqual(valor, -3.3, places=1)

    def test_valor_intrinseco_com_g_limite_inferior(self):
        # Teste com g no limite inferior da conversão decimal (-0.99)
        valor = calcular_valor_intrinseco(lpa=1.0, g=-0.99, selic=10.0)
        self.assertAlmostEqual(valor, -83.38, places=2)

    def test_valor_intrinseco_com_g_limite_superior(self):
        # Teste com g no limite superior da conversão decimal (0.99)
        valor = calcular_valor_intrinseco(lpa=1.0, g=0.99, selic=10.0)
        self.assertAlmostEqual(valor, 90.86, places=2)

    def test_valor_intrinseco_com_g_fora_limite(self):
        # Teste com g fora do limite da conversão decimal (1.0)
        valor = calcular_valor_intrinseco(lpa=1.0, g=1.0, selic=10.0)
        self.assertAlmostEqual(valor, 4.62, places=2)

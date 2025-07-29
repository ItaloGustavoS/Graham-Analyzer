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

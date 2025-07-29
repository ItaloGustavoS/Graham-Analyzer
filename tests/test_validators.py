import unittest
from utils.validators import validar_ticker


class TestValidator(unittest.TestCase):
    def test_ticker_valido(self):
        self.assertTrue(validar_ticker("PETR4"))
        self.assertTrue(validar_ticker("VALE3"))

    def test_ticker_invalido(self):
        self.assertFalse(validar_ticker("!petr4"))
        self.assertFalse(validar_ticker("AB"))  # muito curto
        self.assertFalse(validar_ticker("123@"))

import unittest

from miracle_compiler.compiler import resultado_compilacao


class TestWebSerialization(unittest.TestCase):
    def test_resultado_compilacao_retorna_json_serializavel(self):
        resultado = resultado_compilacao(
            """
DEFINIR(bpm, 120);
DEFINIR(pin, 8);
NOTA(C, 500);
"""
        )

        self.assertTrue(resultado["sucesso"])
        self.assertIn("tokens", resultado)
        self.assertEqual(resultado["ast"]["tipo"], "ProgramNode")
        self.assertEqual(resultado["ast"]["comandos"][0]["tipo"], "DefinirNode")
        self.assertEqual(resultado["ast"]["comandos"][2]["tipo"], "NotaNode")
        self.assertEqual(resultado["tabela_simbolos"]["bpm"]["valor"], 120)
        self.assertEqual(resultado["tabela_simbolos"]["pin"]["valor"], 8)
        self.assertEqual(resultado["erros"], [])
        self.assertIn("codigo_arduino", resultado)
        self.assertIn("const int BUZZER_PIN = 8;", resultado["codigo_arduino"])


if __name__ == "__main__":
    unittest.main()

import unittest

from miracle_compiler.compiler import resultado_compilacao


class TestArduinoCodegen(unittest.TestCase):
    def test_programa_valido_gera_sketch_completo(self):
        resultado = resultado_compilacao(
            """
DEFINIR(pin, 8);
DEFINIR(volume, 80);
NOTA(C, 500);
ESPERAR(250);
"""
        )

        codigo = resultado["codigo_arduino"]

        self.assertTrue(resultado["sucesso"])
        self.assertIn("const int BUZZER_PIN = 8;", codigo)
        self.assertIn("const int VOLUME = 80;", codigo)
        self.assertIn("void setup()", codigo)
        self.assertIn("void loop()", codigo)
        self.assertIn("tone(BUZZER_PIN, frequency);", codigo)
        self.assertIn("playTone(NOTE_C4, 500);", codigo)
        self.assertIn("delay(250);", codigo)

    def test_nota_sem_oitava_usa_quarta_oitava(self):
        resultado = resultado_compilacao(
            """
DEFINIR(pin, 8);
NOTA(C, 500);
"""
        )

        self.assertIn("const int NOTE_C4 = 262;", resultado["codigo_arduino"])
        self.assertIn("playTone(NOTE_C4, 500);", resultado["codigo_arduino"])

    def test_sustenido_e_bemol_equivalentes(self):
        sustenido = resultado_compilacao(
            """
DEFINIR(pin, 8);
NOTA(C#4, 500);
"""
        )
        bemol = resultado_compilacao(
            """
DEFINIR(pin, 8);
NOTA(Db4, 500);
"""
        )

        self.assertIn("const int NOTE_CS4 = 277;", sustenido["codigo_arduino"])
        self.assertIn("const int NOTE_CS4 = 277;", bemol["codigo_arduino"])

    def test_repetir_gera_for(self):
        resultado = resultado_compilacao(
            """
DEFINIR(pin, 8);
REPETIR(3) {
    NOTA(E, 500);
}
"""
        )

        self.assertIn("for (int i = 0; i < 3; i++) {", resultado["codigo_arduino"])
        self.assertIn("playTone(NOTE_E4, 500);", resultado["codigo_arduino"])

    def test_sem_pin_nao_gera_codigo_arduino(self):
        resultado = resultado_compilacao("NOTA(C, 500);")

        self.assertFalse(resultado["sucesso"])
        self.assertIsNone(resultado["codigo_arduino"])
        self.assertTrue(
            any("pin" in erro["mensagem"] for erro in resultado["erros"])
        )

    def test_erro_sintatico_nao_gera_codigo_arduino(self):
        resultado = resultado_compilacao("DEFINIR(pin, 8);\nNOTA(C, 500)")

        self.assertFalse(resultado["sucesso"])
        self.assertIsNone(resultado["codigo_arduino"])


if __name__ == "__main__":
    unittest.main()

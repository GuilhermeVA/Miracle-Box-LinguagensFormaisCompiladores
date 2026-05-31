import unittest

from miracle_compiler.compiler import compilar
from miracle_compiler.frontend.scanner import TOK_EOF


class TestCompiladorMiracle(unittest.TestCase):
    def test_programa_valido_gera_ast_e_tabela(self):
        codigo = """
DEFINIR(bpm, 120);
DEFINIR(volume, 80);
DEFINIR(pin, 8);
REPETIR(2) {
    NOTA(C, 500);
    ESPERAR(250);
}
"""

        tokens, ast, tabela, erros = compilar(codigo)

        self.assertFalse(erros.tem_erros())
        self.assertEqual(tokens[-1].tipo, TOK_EOF)
        self.assertEqual(len(ast.comandos), 4)
        self.assertEqual(tabela.obter("bpm")["valor"], 120)
        self.assertEqual(tabela.obter("volume")["valor"], 80)
        self.assertEqual(tabela.obter("pin")["valor"], 8)

    def test_erro_lexico(self):
        _, ast, _, erros = compilar("NOTA(C, 500); @")

        self.assertIsNone(ast)
        self.assertTrue(erros.tem_erros_lexicos())

    def test_erro_sintatico(self):
        _, ast, _, erros = compilar("NOTA(C, 500)")

        self.assertIsNotNone(ast)
        self.assertTrue(erros.tem_erros_sintaticos())

    def test_erro_semantico_em_bpm_fora_da_faixa(self):
        _, ast, tabela, erros = compilar(
            """
DEFINIR(pin, 8);
DEFINIR(bpm, 500);
"""
        )

        self.assertIsNotNone(ast)
        self.assertIsNone(tabela.obter("bpm"))
        self.assertTrue(erros.tem_erros_semanticos())

    def test_erro_semantico_em_redefinicao(self):
        _, _, tabela, erros = compilar(
            """
DEFINIR(pin, 8);
DEFINIR(pin, 9);
"""
        )

        self.assertEqual(tabela.obter("pin")["valor"], 8)
        self.assertTrue(erros.tem_erros_semanticos())

    def test_erro_semantico_sem_pin(self):
        _, ast, tabela, erros = compilar("NOTA(C, 500);")

        self.assertIsNotNone(ast)
        self.assertIsNone(tabela.obter("pin"))
        self.assertTrue(erros.tem_erros_semanticos())


if __name__ == "__main__":
    unittest.main()

import unittest

from web.app import app


class TestAppFlask(unittest.TestCase):
    def test_index_renderiza(self):
        client = app.test_client()
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Miracle Compiler", response.data)

    def test_compilar_retorna_json(self):
        client = app.test_client()
        response = client.post(
            "/compilar", json={"codigo": "DEFINIR(pin, 8);\nNOTA(C, 500);"}
        )
        dados = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(dados["sucesso"])
        self.assertEqual(dados["ast"]["tipo"], "ProgramNode")
        self.assertEqual(dados["tokens"][0]["tipo"], "TOK_DEFINIR")
        self.assertIn("void loop()", dados["codigo_arduino"])


if __name__ == "__main__":
    unittest.main()

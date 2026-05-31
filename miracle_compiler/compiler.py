from dataclasses import fields, is_dataclass

from miracle_compiler.core.errors import ErrorManager
from miracle_compiler.core.symbols import SymbolTable
from miracle_compiler.frontend.parser import Parser
from miracle_compiler.frontend.scanner import Scanner
from miracle_compiler.analysis.semantic import SemanticAnalyzer
from miracle_compiler.generators.arduino import gerar_codigo_arduino


codigo_miracle_box_1 = """$ Isso e um comentario
DEFINIR(pin, 8);
NOTA(C, 500); $ Toca Do por 500ms
ESPERAR(250); $ Pausa de 250ms
NOTA(E, 500); $ Toca Mi por 500ms
"""

codigo_miracle_box_2 = """$ Testando
DEFINIR(pin, 8);
NOTA(C, 500);
$ Fim do teste
"""

codigo_miracle_box_3 = """$ Isso e um comentario
DEFINIR(pin, 8);
DEFINIR(bpm, 120);
DEFINIR(volume, 80);
REPETIR(4) {
    NOTA(C, 500);
    ESPERAR(250);
    NOTA(E, 500);
}
"""


def compilar(codigo_fonte):
    erros = ErrorManager()
    tokens = Scanner(codigo_fonte, erros).scan()
    ast = None
    tabela = SymbolTable()

    if not erros.tem_erros_lexicos():
        ast = Parser(tokens, erros).parse()

    if ast is not None and not erros.tem_erros_lexicos_ou_sintaticos():
        SemanticAnalyzer(tabela, erros).analyze(ast)

    return tokens, ast, tabela, erros


def serializar_ast(node):
    if node is None:
        return None

    if isinstance(node, list):
        return [serializar_ast(item) for item in node]

    if is_dataclass(node):
        dados = {
            campo.name: serializar_ast(getattr(node, campo.name))
            for campo in fields(node)
        }
        dados["tipo"] = node.__class__.__name__
        return dados

    return node


def resultado_compilacao(codigo_fonte):
    tokens, ast, tabela, erros = compilar(codigo_fonte)
    codigo_arduino = None

    if ast is not None and not erros.tem_erros():
        codigo_arduino = gerar_codigo_arduino(ast, tabela)

    return {
        "tokens": [
            {
                "tipo": token.tipo,
                "valor": token.valor,
                "linha": token.linha,
                "coluna": token.coluna,
            }
            for token in tokens
        ],
        "ast": serializar_ast(ast),
        "tabela_simbolos": tabela.simbolos,
        "erros": [
            {
                "tipo": erro.tipo,
                "mensagem": erro.mensagem,
                "linha": erro.linha,
                "coluna": erro.coluna,
                "texto": str(erro),
            }
            for erro in erros.erros
        ],
        "sucesso": not erros.tem_erros(),
        "codigo_arduino": codigo_arduino,
    }


def executar_exemplo():
    tokens, ast, tabela, erros = compilar(codigo_miracle_box_3)

    print("TOKENS:")
    for token in tokens:
        print(token)

    print("\nAST:")
    print(ast)

    print("\nTABELA DE SIMBOLOS:")
    print(tabela)

    print("\nERROS:")
    erros.exibir()


if __name__ == "__main__":
    executar_exemplo()

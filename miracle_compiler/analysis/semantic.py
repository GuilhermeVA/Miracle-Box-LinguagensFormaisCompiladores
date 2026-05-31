from miracle_compiler.core.ast_nodes import (
    DefinirNode,
    EsperarNode,
    NotaNode,
    ProgramNode,
    RepetirNode,
)
from miracle_compiler.core.errors import ErrorManager
from miracle_compiler.core.music import normalizar_tom
from miracle_compiler.core.symbols import SymbolTable


NOTAS_VALIDAS = {"C", "D", "E", "F", "G", "A", "B"}
CAMPOS_PERMITIDOS = {"bpm", "volume", "pin"}


class SemanticAnalyzer:
    def __init__(self, tabela: SymbolTable, erros: ErrorManager):
        self.tabela = tabela
        self.erros = erros

    def analyze(self, ast):
        self.visitar(ast)
        if not self.tabela.existe("pin"):
            self.erros.erro_semantico("campo 'pin' deve ser definido para gerar Arduino", 1)

    def visitar(self, node):
        if isinstance(node, ProgramNode):
            for comando in node.comandos:
                self.visitar(comando)
        elif isinstance(node, DefinirNode):
            self.visitar_definir(node)
        elif isinstance(node, NotaNode):
            self.visitar_nota(node)
        elif isinstance(node, EsperarNode):
            self.visitar_esperar(node)
        elif isinstance(node, RepetirNode):
            self.visitar_repetir(node)

    def visitar_definir(self, node):
        if node.campo not in CAMPOS_PERMITIDOS:
            self.erros.erro_semantico(
                f"campo desconhecido '{node.campo}' em DEFINIR", node.linha
            )
            return

        if self.tabela.existe(node.campo):
            simbolo = self.tabela.obter(node.campo)
            self.erros.erro_semantico(
                f"campo '{node.campo}' ja definido na linha {simbolo['linha']}",
                node.linha,
            )
            return

        if node.valor <= 0 and node.campo != "volume":
            self.erros.erro_semantico(
                f"valor de '{node.campo}' deve ser maior que zero", node.linha
            )
            return

        if node.campo == "bpm" and not 30 <= node.valor <= 300:
            self.erros.erro_semantico("bpm deve estar entre 30 e 300", node.linha)
            return

        if node.campo == "volume" and not 0 <= node.valor <= 100:
            self.erros.erro_semantico("volume deve estar entre 0 e 100", node.linha)
            return

        self.tabela.definir(node.campo, node.valor, node.linha)

    def visitar_nota(self, node):
        nota_base = node.tom[0]
        if nota_base not in NOTAS_VALIDAS or normalizar_tom(node.tom) is None:
            self.erros.erro_semantico(f"nota invalida '{node.tom}'", node.linha)

        if node.duracao <= 0:
            self.erros.erro_semantico(
                "duracao da nota deve ser maior que zero", node.linha
            )

    def visitar_esperar(self, node):
        if node.duracao <= 0:
            self.erros.erro_semantico(
                "tempo de espera deve ser maior que zero", node.linha
            )

    def visitar_repetir(self, node):
        if node.vezes <= 0:
            self.erros.erro_semantico(
                "quantidade de repeticoes deve ser maior que zero", node.linha
            )

        if not node.conteudo:
            self.erros.erro_semantico("bloco REPETIR nao pode estar vazio", node.linha)

        for comando in node.conteudo:
            self.visitar(comando)

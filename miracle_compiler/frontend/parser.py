from miracle_compiler.core.ast_nodes import (
    DefinirNode,
    EsperarNode,
    NotaNode,
    ProgramNode,
    RepetirNode,
)
from miracle_compiler.core.errors import ErrorManager
from miracle_compiler.frontend.scanner import (
    TOK_DEFINIR,
    TOK_EOF,
    TOK_ESPERAR,
    TOK_ID,
    TOK_LCHAVE,
    TOK_LPAREN,
    TOK_NOTA,
    TOK_NUM,
    TOK_PVIRG,
    TOK_RCHAVE,
    TOK_REPETIR,
    TOK_RPAREN,
    TOK_TOM,
    TOK_VIRGULA,
)


class Parser:
    def __init__(self, tokens, erros: ErrorManager | None = None):
        self.tokens = tokens
        self.erros = erros or ErrorManager()
        self.pos = 0

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def avancar(self):
        token = self.token_atual()
        if token.tipo != TOK_EOF:
            self.pos += 1
        return token

    def consumir(self, tipo_esperado):
        token = self.token_atual()
        if token.tipo == tipo_esperado:
            return self.avancar()

        self.erros.erro_sintatico(
            f"esperava {tipo_esperado}, mas encontrou {token.tipo}",
            token.linha,
            token.coluna,
        )
        return None

    def parse(self):
        return self.parse_programa()

    def parse_programa(self):
        comandos = []
        while self.token_atual().tipo != TOK_EOF:
            comando = self.parse_comando()
            if comando is not None:
                comandos.append(comando)
        return ProgramNode(comandos=comandos)

    def parse_comando(self):
        token = self.token_atual()

        if token.tipo == TOK_DEFINIR:
            return self.parse_definir()
        if token.tipo == TOK_REPETIR:
            return self.parse_repetir()
        if token.tipo == TOK_NOTA:
            return self.parse_nota()
        if token.tipo == TOK_ESPERAR:
            return self.parse_esperar()

        self.erros.erro_sintatico(
            f"comando inesperado {token.valor!r}", token.linha, token.coluna
        )
        self.sincronizar()
        return None

    def parse_definir(self):
        inicio = self.consumir(TOK_DEFINIR)
        self.consumir(TOK_LPAREN)
        campo = self.consumir(TOK_ID)
        self.consumir(TOK_VIRGULA)
        valor = self.consumir(TOK_NUM)
        self.consumir(TOK_RPAREN)
        self.consumir(TOK_PVIRG)

        if campo is None or valor is None:
            self.sincronizar()
            return None

        return DefinirNode(campo=campo.valor, valor=valor.valor, linha=inicio.linha)

    def parse_repetir(self):
        inicio = self.consumir(TOK_REPETIR)
        self.consumir(TOK_LPAREN)
        vezes = self.consumir(TOK_NUM)
        self.consumir(TOK_RPAREN)
        self.consumir(TOK_LCHAVE)

        comandos = []
        while self.token_atual().tipo not in (TOK_RCHAVE, TOK_EOF):
            comando = self.parse_comando()
            if comando is not None:
                comandos.append(comando)

        self.consumir(TOK_RCHAVE)

        if vezes is None:
            self.sincronizar()
            return None

        return RepetirNode(vezes=vezes.valor, conteudo=comandos, linha=inicio.linha)

    def parse_nota(self):
        inicio = self.consumir(TOK_NOTA)
        self.consumir(TOK_LPAREN)
        tom = self.consumir(TOK_TOM)
        self.consumir(TOK_VIRGULA)
        duracao = self.consumir(TOK_NUM)
        self.consumir(TOK_RPAREN)
        self.consumir(TOK_PVIRG)

        if tom is None or duracao is None:
            self.sincronizar()
            return None

        return NotaNode(tom=tom.valor, duracao=duracao.valor, linha=inicio.linha)

    def parse_esperar(self):
        inicio = self.consumir(TOK_ESPERAR)
        self.consumir(TOK_LPAREN)
        duracao = self.consumir(TOK_NUM)
        self.consumir(TOK_RPAREN)
        self.consumir(TOK_PVIRG)

        if duracao is None:
            self.sincronizar()
            return None

        return EsperarNode(duracao=duracao.valor, linha=inicio.linha)

    def sincronizar(self):
        while self.token_atual().tipo not in (TOK_PVIRG, TOK_RCHAVE, TOK_EOF):
            self.avancar()
        if self.token_atual().tipo == TOK_PVIRG:
            self.avancar()

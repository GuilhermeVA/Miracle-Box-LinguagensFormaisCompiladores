import re
from dataclasses import dataclass

from miracle_compiler.core.errors import ErrorManager


TOK_NOTA = "TOK_NOTA"
TOK_DEFINIR = "TOK_DEFINIR"
TOK_ESPERAR = "TOK_ESPERAR"
TOK_REPETIR = "TOK_REPETIR"
TOK_NUM = "TOK_NUM"
TOK_TOM = "TOK_TOM"
TOK_ID = "TOK_ID"
TOK_LPAREN = "TOK_LPAREN"
TOK_RPAREN = "TOK_RPAREN"
TOK_LCHAVE = "TOK_LCHAVE"
TOK_RCHAVE = "TOK_RCHAVE"
TOK_PVIRG = "TOK_PVIRG"
TOK_VIRGULA = "TOK_VIRGULA"
TOK_EOF = "TOK_EOF"


@dataclass
class Token:
    tipo: str
    valor: object
    linha: int
    coluna: int

    def __repr__(self):
        return (
            f"Token({self.tipo}, {self.valor!r}, "
            f"linha={self.linha}, coluna={self.coluna})"
        )


ESPECIFICACAO_TOKENS = [
    (TOK_NOTA, r"NOTA\b"),
    (TOK_DEFINIR, r"DEFINIR\b"),
    (TOK_ESPERAR, r"ESPERAR\b"),
    (TOK_REPETIR, r"REPETIR\b"),
    (TOK_NUM, r"\d+"),
    (TOK_TOM, r"[A-G][#b]?[0-8]?"),
    (TOK_ID, r"[a-z][a-z0-9_]*"),
    (TOK_LPAREN, r"\("),
    (TOK_RPAREN, r"\)"),
    (TOK_LCHAVE, r"\{"),
    (TOK_RCHAVE, r"\}"),
    (TOK_PVIRG, r";"),
    (TOK_VIRGULA, r","),
    ("TOK_COMENT", r"\$[^\n]*"),
    ("SKIP", r"[ \t]+"),
    ("NEWLINE", r"\n"),
    ("MISMATCH", r"."),
]


class Scanner:
    def __init__(self, codigo_fonte, erros: ErrorManager):
        self.codigo_fonte = codigo_fonte
        self.erros = erros
        self.regex_unida = re.compile(
            "|".join(f"(?P<{nome}>{regex})" for nome, regex in ESPECIFICACAO_TOKENS)
        )

    def scan(self):
        linha = 1
        inicio_linha = 0
        tokens = []

        for match in self.regex_unida.finditer(self.codigo_fonte):
            tipo = match.lastgroup
            valor = match.group()
            coluna = match.start() - inicio_linha + 1

            if tipo == TOK_NUM:
                tokens.append(Token(tipo, int(valor), linha, coluna))
            elif tipo in ("SKIP", "TOK_COMENT"):
                continue
            elif tipo == "NEWLINE":
                linha += 1
                inicio_linha = match.end()
            elif tipo == "MISMATCH":
                self.erros.erro_lexico(f"caractere invalido '{valor}'", linha, coluna)
            else:
                tokens.append(Token(tipo, valor, linha, coluna))

        tokens.append(Token(TOK_EOF, None, linha, 1))
        return tokens


def analisador_lexico(codigo_fonte):
    erros = ErrorManager()
    tokens = Scanner(codigo_fonte, erros).scan()
    erros.exibir()
    return [token for token in tokens if token.tipo != TOK_EOF]

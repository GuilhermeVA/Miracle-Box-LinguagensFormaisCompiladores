from dataclasses import dataclass


LEXICO = "LEXICO"
SINTATICO = "SINTATICO"
SEMANTICO = "SEMANTICO"


@dataclass
class CompileError:
    tipo: str
    mensagem: str
    linha: int
    coluna: int | None = None

    def __str__(self):
        local = f"Linha {self.linha}"
        if self.coluna is not None:
            local += f", coluna {self.coluna}"
        return f"[{self.tipo}] {local}: {self.mensagem}"


class ErrorManager:
    def __init__(self):
        self.erros = []

    def adicionar(self, tipo, mensagem, linha, coluna=None):
        self.erros.append(CompileError(tipo, mensagem, linha, coluna))

    def erro_lexico(self, mensagem, linha, coluna=None):
        self.adicionar(LEXICO, mensagem, linha, coluna)

    def erro_sintatico(self, mensagem, linha, coluna=None):
        self.adicionar(SINTATICO, mensagem, linha, coluna)

    def erro_semantico(self, mensagem, linha, coluna=None):
        self.adicionar(SEMANTICO, mensagem, linha, coluna)

    def tem_erros(self):
        return bool(self.erros)

    def tem_erros_lexicos(self):
        return any(erro.tipo == LEXICO for erro in self.erros)

    def tem_erros_sintaticos(self):
        return any(erro.tipo == SINTATICO for erro in self.erros)

    def tem_erros_semanticos(self):
        return any(erro.tipo == SEMANTICO for erro in self.erros)

    def tem_erros_lexicos_ou_sintaticos(self):
        return self.tem_erros_lexicos() or self.tem_erros_sintaticos()

    def exibir(self):
        if not self.erros:
            print("Nenhum erro encontrado.")
            return

        for erro in self.erros:
            print(erro)

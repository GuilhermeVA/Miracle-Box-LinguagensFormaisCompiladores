import re

# Exemplos de código .song
codigo_miracle_box_1 = """$ Isso é um comentário
NOTA(C, 500); $Toca Dó por 500ms
ESPERAR(250); $ Pausa de 250ms
NOTA(E, 500); $ Toca Mi por 500ms
"""

codigo_miracle_box_2 = """ $ Testando
NOTA(C, 500);
$Fim do teste

"""

codigo_miracle_box_3 = """$Isso é um comentário
DEFINIR(bpm, 120);
REPETIR(4) {
    NOTA(C, 500); $Toca Dó por 500ms
    ESPERAR(250); $ Pausa de 250ms
    NOTA(E, 500); $ Toca Mi por 500ms
}


"""

# ------------------------------------------------------------------------------------------------------------------
# Tokens
class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, linha={self.linha})"


# ------------------------------------------------------------------------------------------------------------------
# Nós da AST
class Programa:
    def __init__(self, comandos):
        self.comandos = comandos

    def __repr__(self):
        return f"Programa({self.comandos})"


class Definir:
    def __init__(self, propriedade, valor):
        self.propriedade = propriedade
        self.valor = valor

    def __repr__(self):
        return f"Definir({self.propriedade!r}, {self.valor})"


class Repetir:
    def __init__(self, vezes, comandos):
        self.vezes = vezes
        self.comandos = comandos

    def __repr__(self):
        return f"Repetir({self.vezes}, {self.comandos})"


class Nota:
    def __init__(self, tom, duracao):
        self.tom = tom
        self.duracao = duracao

    def __repr__(self):
        return f"Nota({self.tom!r}, {self.duracao})"


class Esperar:
    def __init__(self, duracao):
        self.duracao = duracao

    def __repr__(self):
        return f"Esperar({self.duracao})"


class AnalisadorSemantico:
    PROPRIEDADES_VALIDAS = {
        'bpm': (1, 300),
        'volume': (0, 100),
    }

    NOTAS_VALIDAS = {'C', 'D', 'E', 'F', 'G', 'A', 'B'}
    ACIDENTES_VALIDOS = {'#', 'b'}

    def analisar(self, programa):
        for comando in programa.comandos:
            self.analisar_comando(comando)

    def analisar_comando(self, comando):
        if isinstance(comando, Definir):
            self.analisar_definir(comando)
        elif isinstance(comando, Repetir):
            self.analisar_repetir(comando)
        elif isinstance(comando, Nota):
            self.analisar_nota(comando)
        elif isinstance(comando, Esperar):
            self.analisar_esperar(comando)
        else:
            raise Exception(f"Erro Semantico: Comando desconhecido {comando}")

    def analisar_definir(self, comando):
        if comando.propriedade not in self.PROPRIEDADES_VALIDAS:
            propriedades = ', '.join(self.PROPRIEDADES_VALIDAS)
            raise Exception(
                f"Erro Semantico: Propriedade {comando.propriedade!r} nao existe. "
                f"Use uma destas: {propriedades}"
            )

        minimo, maximo = self.PROPRIEDADES_VALIDAS[comando.propriedade]
        if not minimo <= comando.valor <= maximo:
            raise Exception(
                f"Erro Semantico: Valor de {comando.propriedade!r} deve estar "
                f"entre {minimo} e {maximo}"
            )

    def analisar_repetir(self, comando):
        if comando.vezes <= 0:
            raise Exception("Erro Semantico: REPETIR deve executar ao menos 1 vez")

        for comando_interno in comando.comandos:
            self.analisar_comando(comando_interno)

    def analisar_nota(self, comando):
        if not self.tom_valido(comando.tom):
            raise Exception(f"Erro Semantico: Nota musical invalida {comando.tom!r}")

        self.validar_duracao(comando.duracao, 'NOTA')

    def analisar_esperar(self, comando):
        self.validar_duracao(comando.duracao, 'ESPERAR')

    def validar_duracao(self, duracao, comando):
        if duracao <= 0:
            raise Exception(f"Erro Semantico: Duracao de {comando} deve ser maior que 0")

    def tom_valido(self, tom):
        nota = tom[0]
        restante = tom[1:]

        if nota not in self.NOTAS_VALIDAS:
            return False

        if not restante:
            return True

        if restante[0] in self.ACIDENTES_VALIDOS:
            restante = restante[1:]

        if not restante:
            return True

        return restante.isdigit() and 0 <= int(restante) <= 8


# ------------------------------------------------------------------------------------------------------------------
# Definição dos tokens - Lista de tuplas: (Nome do Token, Expressão Regular)
ESPECIFICACAO_TOKENS = [
    ('TOK_NOTA',     r'NOTA'),             # Palavra-chave específica
    ('TOK_DEFINIR',  r'DEFINIR'),          # Palavra-chave específica
    ('TOK_ESPERAR',  r'ESPERAR'),          # Palavra-chave específica
    ('TOK_REPETIR',  r'REPETIR'),          # Palavra-chave específica
    ('TOK_NUM',      r'\d+'),              # Números inteiros
    ('TOK_TOM',      r'[A-Z][#b]?[0-9]*'), # Notas musicais: C, F#, Ab3
    ('TOK_ID',       r'[a-z][a-z0-9_]*'),  # Identificadores: bpm, volume
    ('TOK_LPAREN',   r'\('),               # Símbolo (
    ('TOK_RPAREN',   r'\)'),               # Símbolo )
    ('TOK_LCHAVE',   r'\{'),               # Símbolo {
    ('TOK_RCHAVE',   r'\}'),               # Símbolo }
    ('TOK_PVIRG',    r';'),                # Fim de comando ;
    ('TOK_VIRGULA',  r','),                # Separador ,
    ('TOK_COMENT',   r'\$.*'),             # Comentários com $
    ('SKIP',         r'[ \t]+'),           # Espaços e tabs
    ('NEWLINE',      r'\r?\n'),            # Quebra de linha
    ('MISMATCH',     r'.'),                # Qualquer outro caractere inválido
]


# ------------------------------------------------------------------------------------------------------------------
# Função do analisador léxico - Geração de tokens
def analisador_lexico(codigo_fonte):
    linha_atual = 1
    tokens = []

    regex_unida = '|'.join(
        f'(?P<{nome}>{regex})' for nome, regex in ESPECIFICACAO_TOKENS
    )

    for mo in re.finditer(regex_unida, codigo_fonte):
        tipo = mo.lastgroup
        valor = mo.group()

        if tipo == 'TOK_NUM':
            tokens.append(Token(tipo, int(valor), linha_atual))
        elif tipo in ('SKIP', 'TOK_COMENT'):
            continue
        elif tipo == 'NEWLINE':
            linha_atual += 1
        elif tipo == 'MISMATCH':
            raise Exception(
                f"ERRO LÉXICO: Caractere inválido {valor!r} na linha {linha_atual}"
            )
        else:
            tokens.append(Token(tipo, valor, linha_atual))

    return tokens


# ------------------------------------------------------------------------------------------------------------------
# Analisador sintático - Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, tipo_esperado):
        token = self.token_atual()

        if token and token.tipo == tipo_esperado:
            self.pos += 1
            return token

        encontrado = token.tipo if token else 'FIM'
        linha = token.linha if token else '?'
        raise Exception(
            f"Erro Sintático: Esperava {tipo_esperado}, mas encontrei {encontrado} na linha {linha}"
        )

    def parse_programa(self):
        comandos = []

        while self.token_atual() is not None:
            comandos.append(self.parse_comando())

        return Programa(comandos)

    def parse_comando(self):
        token = self.token_atual()

        if token is None:
            raise Exception("Erro Sintático: Fim inesperado do código")

        if token.tipo == 'TOK_DEFINIR':
            return self.parse_definir()
        elif token.tipo == 'TOK_REPETIR':
            return self.parse_repetir()
        elif token.tipo == 'TOK_NOTA':
            return self.parse_nota()
        elif token.tipo == 'TOK_ESPERAR':
            return self.parse_esperar()

        raise Exception(
            f"Erro Sintático na linha {token.linha}: Comando inesperado {token.valor!r}"
        )

    def parse_definir(self):
        self.consumir('TOK_DEFINIR')
        self.consumir('TOK_LPAREN')
        propriedade = self.consumir('TOK_ID').valor
        self.consumir('TOK_VIRGULA')
        valor = self.consumir('TOK_NUM').valor
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')

        return Definir(propriedade, valor)

    def parse_repetir(self):
        self.consumir('TOK_REPETIR')
        self.consumir('TOK_LPAREN')
        vezes = self.consumir('TOK_NUM').valor
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_LCHAVE')

        comandos_internos = []

        while self.token_atual() and self.token_atual().tipo != 'TOK_RCHAVE':
            comandos_internos.append(self.parse_comando())

        self.consumir('TOK_RCHAVE')

        return Repetir(vezes, comandos_internos)

    def parse_nota(self):
        self.consumir('TOK_NOTA')
        self.consumir('TOK_LPAREN')
        tom = self.consumir('TOK_TOM').valor
        self.consumir('TOK_VIRGULA')
        duracao = self.consumir('TOK_NUM').valor
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')

        return Nota(tom, duracao)

    def parse_esperar(self):
        self.consumir('TOK_ESPERAR')
        self.consumir('TOK_LPAREN')
        duracao = self.consumir('TOK_NUM').valor
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')

        return Esperar(duracao)


# ------------------------------------------------------------------------------------------------------------------
# Execução de teste
if __name__ == '__main__':
    tokens = analisador_lexico(codigo_miracle_box_3)
    parser = Parser(tokens)
    programa = parser.parse_programa()
    analisador_semantico = AnalisadorSemantico()
    analisador_semantico.analisar(programa)

    print(programa)

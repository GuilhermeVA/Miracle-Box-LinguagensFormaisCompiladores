import re

#Exemplos de código .song
codigo_miracle_box_1 = """$ Isso é um comentário
NOTA(C, 500); $Toca Dó por 500ms
ESPERAR(250); $ Pausa de 250ms
NOTA(E, 500); $ Toca Mi por 500ms
"""

codigo_miracle_box_2 = """ $ Testando
123
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


#Definição do o que é um token
class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}', linha={self.linha})"
    

# Definição dos tokens - Lista de tuplas: (Nome do Token, Expressão Regular)
ESPECIFICACAO_TOKENS = [
    ('TOK_NOTA',     r'NOTA'),           # Palavra-chave específica
    ('TOK_DEFINIR',  r'DEFINIR'),        # Palavra-chave específica
    ('TOK_ESPERAR',  r'ESPERAR'),        # Palavra-chave específica
    ('TOK_REPETIR',  r'REPETIR'),
    ('TOK_NUM',      r'\d+'),            # Números (inteiros)
    ('TOK_TOM',      r'[A-G][#b]?[0-8]?'), # Notas musicais (C, F#, Ab3)
    ('TOK_ID',       r'[a-z][a-z0-9_]*'), # Identificadores (bpm, volume)
    ('TOK_LPAREN',   r'\('),             # Símbolo (
    ('TOK_RPAREN',   r'\)'),             # Símbolo )
    ('TOK_LCHAVE',   r'\{'),             # Símbolo (
    ('TOK_RCHAVE',   r'\}'),             # Símbolo )
    ('TOK_PVIRG',    r';'),              # Fim de linha ;
    ('TOK_VIRGULA',  r','),              # Separador ,
    ('TOK_COMENT',   r'\$.*'),           # Comentários com $
    ('SKIP',         r'[ \t]+'),         # Espaços e tabs (para ignorar)
    ('NEWLINE',      r'\n'),             # Quebra de linha (para contar a linha atual)
    ('MISMATCH',     r'.'),              # Qualquer outro caractere (Erro!)
]


#Função do análisador léxico - Geração de tokens
def analisador_lexico(codigo_fonte):
    linha_atual = 1
    tokens = []
    
    # Transforma nossos tokens em um padrão, unindo todas a regex
    regex_unida = '|'.join(f'(?P<{par[0]}>{par[1]})' for par in ESPECIFICACAO_TOKENS)
    
    # Loop que varre a string buscando matches através do padrão que definimos
    for mo in re.finditer(regex_unida, codigo_fonte):
        tipo = mo.lastgroup
        valor = mo.group()


        if tipo == 'TOK_NUM':
            tokens.append(Token(tipo, int(valor), linha_atual))
        elif tipo == 'SKIP' or tipo == 'TOK_COMENT':
            continue
        elif tipo == 'NEWLINE':
            linha_atual += 1
        elif tipo == 'MISMATCH':
            print(f"ERRO LÉXICO: Caractere inválido '{valor}' na linha {linha_atual}")
        else:
            # Para palavras-chave, IDs e símbolos
            tokens.append(Token(tipo, valor, linha_atual))
            
    return tokens



print(analisador_lexico(codigo_miracle_box_3))

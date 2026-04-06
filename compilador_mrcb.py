import re

#Exemplos de código .song
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
#Tokens
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


# ------------------------------------------------------------------------------------------------------------------
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



#print(analisador_lexico(codigo_miracle_box_2))



# ------------------------------------------------------------------------------------------------------------------
# Análisador sintático - Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Posição atual na lista de tokens

    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, tipo_esperado):
        #Verifica se o token atual é o esperado e pula para o próximo.
        token = self.token_atual()
        if token and token.tipo == tipo_esperado:
            self.pos += 1
            return token
        else:
            raise Exception(f"Erro Sintático: Esperava {tipo_esperado} mas encontrei {token.tipo if token else 'FIM'} na linha {token.linha if token else '?'}")
    
    def parse_programa(self):
        #Ponto de entrada: lê todos os comandos até o fim dos tokens
        ast = []
        while self.token_atual() is not None:
            ast.append(self.parse_comando())
        return ast

    def parse_comando(self):
        token = self.token_atual()
        if token.tipo == 'TOK_DEFINIR':
            return self.parse_definir()
        elif token.tipo == 'TOK_REPETIR':
            return self.parse_repetir()
        elif token.tipo == 'TOK_NOTA':
            return self.parse_nota()
        elif token.tipo == 'TOK_ESPERAR':
            return self.parse_esperar()
        else:
            raise Exception(f"Erro Sintático na linha {token.linha}: Comando inesperado {token.valor}")
        


    #Implementação das regras sintáticas
    def parse_definir(self):
        self.consumir('TOK_DEFINIR')
        self.consumir('TOK_LPAREN')
        propriedade = self.consumir('TOK_ID').valor 
        self.consumir('TOK_VIRGULA')
        valor = self.consumir('TOK_NUM').valor       
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')
        return {"acao": "DEFINIR", "campo": propriedade, "valor": valor}

    def parse_repetir(self):
        self.consumir('TOK_REPETIR')
        self.consumir('TOK_LPAREN')
        vezes = self.consumir('TOK_NUM').valor
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_LCHAVE')
        
        # Lista para guardar os comandos que estão dentro do loop
        comandos_internos = []
        
        # Enquanto não encontrar o fecha chaves '}', continua lendo comandos
        while self.token_atual() and self.token_atual().tipo != 'TOK_RCHAVE':
            comandos_internos.append(self.parse_comando())
            
        self.consumir('TOK_RCHAVE')
        return {"acao": "REPETIR", "vezes": vezes, "conteudo": comandos_internos}
    
    def parse_nota(self):
        self.consumir('TOK_NOTA')
        self.consumir('TOK_LPAREN')
        tom = self.consumir('TOK_TOM').valor
        self.consumir('TOK_VIRGULA')
        valor = self.consumir('TOK_NUM').valor       
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')
        return {"acao": "NOTA", "tom": tom, "tempo(ms)": valor}
    
    def parse_esperar(self):
        self.consumir('TOK_ESPERAR')
        self.consumir('TOK_LPAREN')
        valor = self.consumir('TOK_NUM').valor       
        self.consumir('TOK_RPAREN')
        self.consumir('TOK_PVIRG')
        return {"acao": "ESPERAR", "tempo(ms)": valor}
    

parser = Parser(analisador_lexico(codigo_miracle_box_2))
print(parser.parse_programa())

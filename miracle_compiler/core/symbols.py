class SymbolTable:
    def __init__(self):
        self.simbolos = {}

    def definir(self, nome, valor, linha):
        self.simbolos[nome] = {"valor": valor, "linha": linha}

    def existe(self, nome):
        return nome in self.simbolos

    def obter(self, nome):
        return self.simbolos.get(nome)

    def __repr__(self):
        return repr(self.simbolos)

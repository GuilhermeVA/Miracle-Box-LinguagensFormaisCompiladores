from dataclasses import dataclass


@dataclass
class ProgramNode:
    comandos: list
    linha: int = 1


@dataclass
class DefinirNode:
    campo: str
    valor: int
    linha: int


@dataclass
class NotaNode:
    tom: str
    duracao: int
    linha: int


@dataclass
class EsperarNode:
    duracao: int
    linha: int


@dataclass
class RepetirNode:
    vezes: int
    conteudo: list
    linha: int

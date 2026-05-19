# Miracle Box - Linguagem de Programacao Musical

O **Miracle Box** e uma linguagem de dominio especifico criada para escrever pequenas composicoes musicais de forma simples. A proposta do projeto e permitir que comandos como notas, pausas, repeticoes e configuracoes musicais sejam descritos em uma sintaxe propria, que futuramente pode ser traduzida para codigo C++/Arduino e executada em microcontroladores com buzzer.

Este projeto faz parte da disciplina de **Linguagens Formais e Compiladores**.

## Objetivo

O objetivo do compilador e ler um codigo escrito na linguagem Miracle Box, validar sua estrutura e preparar uma representacao interna da musica.

Atualmente o projeto possui:

- analisador lexico;
- analisador sintatico;
- arvore sintatica abstrata, tambem chamada de AST;
- analisador semantico.

O gerador de codigo para Arduino ainda esta previsto como evolucao futura.

## Como Executar

Para executar o compilador, use Python 3:

```bash
python compilador_mrcb.py
```

O arquivo `compilador_mrcb.py` possui exemplos de codigo Miracle Box definidos nas variaveis `codigo_miracle_box_1`, `codigo_miracle_box_2` e `codigo_miracle_box_3`.

No momento, o exemplo executado e este:

```python
tokens = analisador_lexico(codigo_miracle_box_3)
parser = Parser(tokens)
programa = parser.parse_programa()
analisador_semantico = AnalisadorSemantico()
analisador_semantico.analisar(programa)

print(programa)
```

Para testar outro exemplo, altere a variavel passada para `analisador_lexico`.

## Sintaxe da Linguagem

Cada comando da linguagem deve terminar com ponto e virgula `;`, exceto blocos de repeticao, que usam chaves `{ }`.

Comentarios comecam com `$` e vao ate o fim da linha:

```txt
$ Isto e um comentario
```

## Comandos Disponiveis

### NOTA

Toca uma nota musical por uma duracao em milissegundos.

```txt
NOTA(C, 500);
NOTA(F#, 250);
NOTA(Ab3, 1000);
```

Formato:

```txt
NOTA(tom, duracao);
```

Regras:

- o tom deve ser uma nota entre `A` e `G`;
- pode usar acidente `#` ou `b`;
- pode usar oitava de `0` a `8`;
- a duracao deve ser maior que `0`.

### ESPERAR

Cria uma pausa na musica.

```txt
ESPERAR(250);
```

Formato:

```txt
ESPERAR(duracao);
```

Regra:

- a duracao deve ser maior que `0`.

### DEFINIR

Define uma propriedade de configuracao da musica.

```txt
DEFINIR(bpm, 120);
DEFINIR(volume, 80);
```

Formato:

```txt
DEFINIR(propriedade, valor);
```

Propriedades aceitas:

| Propriedade | Valor minimo | Valor maximo |
| --- | ---: | ---: |
| `bpm` | 1 | 300 |
| `volume` | 0 | 100 |

### REPETIR

Repete um bloco de comandos.

```txt
REPETIR(4) {
    NOTA(C, 500);
    ESPERAR(250);
    NOTA(E, 500);
}
```

Formato:

```txt
REPETIR(quantidade) {
    comandos
}
```

Regra:

- a quantidade de repeticoes deve ser maior que `0`.

## Exemplo Completo

```txt
$ Configuracao inicial
DEFINIR(bpm, 120);
DEFINIR(volume, 80);

$ Melodia principal
REPETIR(4) {
    NOTA(C, 500);
    ESPERAR(250);
    NOTA(E, 500);
}
```

## Etapas do Compilador

### 1. Analise Lexica

A funcao `analisador_lexico` recebe o codigo fonte e transforma o texto em tokens.

Exemplo de tokens reconhecidos:

- `TOK_NOTA`;
- `TOK_DEFINIR`;
- `TOK_ESPERAR`;
- `TOK_REPETIR`;
- `TOK_NUM`;
- `TOK_TOM`;
- `TOK_ID`.

Se um caractere invalido for encontrado, o compilador gera um erro lexico.

### 2. Analise Sintatica

A classe `Parser` recebe a lista de tokens e verifica se a ordem dos comandos respeita a gramatica da linguagem.

Ela tambem monta uma AST usando classes como:

- `Programa`;
- `Definir`;
- `Repetir`;
- `Nota`;
- `Esperar`.

Se a estrutura estiver incorreta, o compilador gera um erro sintatico.

### 3. Analise Semantica

A classe `AnalisadorSemantico` verifica se o programa faz sentido de acordo com as regras da linguagem.

Ela valida, por exemplo:

- propriedades permitidas em `DEFINIR`;
- faixas validas para `bpm` e `volume`;
- repeticoes maiores que zero;
- duracoes maiores que zero;
- formato valido das notas musicais.

Se alguma regra de significado for violada, o compilador gera um erro semantico.

## Exemplos de Erros

### Erro lexico

```txt
NOTA(C, 500)@
```

O caractere `@` nao pertence a linguagem.

### Erro sintatico

```txt
NOTA(C 500);
```

Falta a virgula entre a nota e a duracao.

### Erro semantico

```txt
DEFINIR(andamento, 120);
```

A propriedade `andamento` nao existe na linguagem atual.

Outro exemplo:

```txt
REPETIR(0) {
    NOTA(C, 500);
}
```

`REPETIR` deve executar ao menos uma vez.

## Estrutura do Projeto

```txt
Miracle-Box-LinguagensFormaisCompiladores/
|-- compilador_mrcb.py
|-- README.md
```

## Status Atual

O compilador atualmente le, valida e monta a representacao interna dos programas Miracle Box. A proxima etapa natural do projeto e implementar o gerador de codigo para Arduino.

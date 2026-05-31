# 🎵⭐ Miracle: Linguagem de Programação Musical
O Miracle é uma linguagem de domínio específico (DSL) criada para facilitar a composição de melodias em microcontroladores utilizando buzzers. O projeto faz parte da disciplina de Linguagens Formais e Compiladores.

## 🎯 Objetivo
O objetivo do projeto é criar um compilador que lê um arquivo de texto com comandos musicais e o traduz para código C++ (Arduino), permitindo que qualquer pessoa crie músicas sem precisar lidar diretamente com frequências complexas ou cálculos de milissegundos.

## 🛠️ Arquitetura do Projeto
O compilador é dividido em etapas fundamentais:

* Analisador Léxico (Lexer): Utiliza a biblioteca re do Python para identificar tokens como notas, números e comandos através de Expressões Regulares.

* Analisador Sintático (Parser): Valida a estrutura gramatical da música e cria uma AST.

* Árvore de Sintaxe Abstrata (AST): Representa comandos como DEFINIR, NOTA, ESPERAR e REPETIR em classes Python.

* Analisador Semântico: Valida regras como duração positiva, BPM em faixa válida e redefinição de símbolos.

* Tabela de Símbolos: Guarda configurações declaradas por DEFINIR, como bpm, volume e pin.

* Gerenciador de Erros: Centraliza erros léxicos, sintáticos e semânticos com linha e coluna.

* Gerador de Código: Converte a estrutura da linguagem para um sketch Arduino.

## 📁 Organização

```txt
miracle_compiler/
  compiler.py       Orquestra scanner, parser, semântica e geração Arduino
  core/             AST, erros, tabela de símbolos e utilidades musicais
  frontend/         Scanner e parser da linguagem Miracle
  analysis/         Analisador semântico
  generators/       Geradores de código, incluindo Arduino
web/                Aplicação Flask, templates HTML e arquivos CSS/JS
tests/              Testes automatizados do compilador e da interface web
```

## ▶️ Como executar

```bash
python -m miracle_compiler.compiler
```

## 🌐 Interface Web

Instale as dependências e execute o servidor Flask:

```bash
poetry install
poetry run python -m web.app
```

Acesse:

```txt
http://127.0.0.1:5000
```

## ✅ Como testar

```bash
poetry run python -m unittest discover -s tests
```

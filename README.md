# 🎵⭐ Miracle: Linguagem de Programação Musical
O Miracle é uma linguagem de domínio específico (DSL) criada para facilitar a composição de melodias em microcontroladores utilizando buzzers. O projeto faz parte da disciplina de Linguagens Formais e Compiladores.

## 🎯 Objetivo
O objetivo do projeto é criar um compilador que lê um arquivo de texto com comandos musicais e o traduz para código C++ (Arduino), permitindo que qualquer pessoa crie músicas sem precisar lidar diretamente com frequências complexas ou cálculos de milissegundos.

## 🛠️ Arquitetura do Projeto
O compilador é dividido em etapas fundamentais:

* Analisador Léxico (Lexer): Utiliza a biblioteca re do Python para identificar tokens como notas, números e comandos através de Expressões Regulares.

* Analisador Sintático (Parser): (Em desenvolvimento) Valida a estrutura gramatical da música.

* Gerador de Código: (Em desenvolvimento) Converte a estrutura da linguagem para funções do Arduino.

from miracle_compiler.core.ast_nodes import EsperarNode, NotaNode, ProgramNode, RepetirNode
from miracle_compiler.core.music import FREQUENCIAS_NOTAS, normalizar_tom


class ArduinoCodeGenerator:
    def __init__(self, tabela):
        self.tabela = tabela
        self.notas_usadas = {}

    def generate(self, ast):
        corpo = self.gerar_comandos(ast.comandos, nivel=1)
        constantes_notas = self.gerar_constantes_notas()
        pin = self.tabela.obter("pin")["valor"]
        volume = self.tabela.obter("volume")

        linhas = [
            "// Codigo gerado pelo Miracle Compiler",
            "",
            f"const int BUZZER_PIN = {pin};",
        ]

        if volume is not None:
            linhas.extend(
                [
                    f"const int VOLUME = {volume['valor']};",
                    "// VOLUME e informativo: tone() nao controla volume por software.",
                ]
            )

        if constantes_notas:
            linhas.extend(["", *constantes_notas])

        linhas.extend(
            [
                "",
                "void playTone(int frequency, int duration) {",
                "  tone(BUZZER_PIN, frequency);",
                "  delay(duration);",
                "  noTone(BUZZER_PIN);",
                "}",
                "",
                "void setup() {",
                "  pinMode(BUZZER_PIN, OUTPUT);",
                "}",
                "",
                "void loop() {",
                *corpo,
                "}",
                "",
            ]
        )

        return "\n".join(linhas)

    def gerar_comandos(self, comandos, nivel):
        linhas = []
        for comando in comandos:
            linhas.extend(self.gerar_comando(comando, nivel))
        return linhas

    def gerar_comando(self, comando, nivel):
        indentacao = "  " * nivel

        if isinstance(comando, NotaNode):
            tom_normalizado = normalizar_tom(comando.tom)
            constante = f"NOTE_{tom_normalizado}"
            self.notas_usadas[tom_normalizado] = FREQUENCIAS_NOTAS[tom_normalizado]
            return [f"{indentacao}playTone({constante}, {comando.duracao});"]

        if isinstance(comando, EsperarNode):
            return [f"{indentacao}delay({comando.duracao});"]

        if isinstance(comando, RepetirNode):
            linhas = [f"{indentacao}for (int i = 0; i < {comando.vezes}; i++) {{"]
            linhas.extend(self.gerar_comandos(comando.conteudo, nivel + 1))
            linhas.append(f"{indentacao}}}")
            return linhas

        return []

    def gerar_constantes_notas(self):
        return [
            f"const int NOTE_{tom} = {frequencia};"
            for tom, frequencia in sorted(self.notas_usadas.items())
        ]


def gerar_codigo_arduino(ast, tabela):
    if ast is None or not isinstance(ast, ProgramNode):
        return None

    return ArduinoCodeGenerator(tabela).generate(ast)

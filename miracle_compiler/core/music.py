import math


NOMES_NOTAS = {
    0: "C",
    1: "CS",
    2: "D",
    3: "DS",
    4: "E",
    5: "F",
    6: "FS",
    7: "G",
    8: "GS",
    9: "A",
    10: "AS",
    11: "B",
}

SEMITONS_BASE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

ACIDENTES = {
    "#": 1,
    "b": -1,
}


def normalizar_tom(tom):
    base = tom[0]
    restante = tom[1:]
    acidente = ""

    if restante and restante[0] in ACIDENTES:
        acidente = restante[0]
        restante = restante[1:]

    oitava = int(restante) if restante else 4
    semitom = SEMITONS_BASE[base] + ACIDENTES.get(acidente, 0)
    indice = oitava * 12 + semitom

    if indice < 0 or indice > (8 * 12 + 11):
        return None

    oitava_normalizada = indice // 12
    semitom_normalizado = indice % 12
    return f"{NOMES_NOTAS[semitom_normalizado]}{oitava_normalizada}"


def frequencia_para_tom_normalizado(tom_normalizado):
    if tom_normalizado[1] == "S":
        nome = tom_normalizado[:2]
        oitava = int(tom_normalizado[2:])
    else:
        nome = tom_normalizado[0]
        oitava = int(tom_normalizado[1:])

    semitom = next(valor for valor, nota in NOMES_NOTAS.items() if nota == nome)
    midi = (oitava + 1) * 12 + semitom
    return round(440 * math.pow(2, (midi - 69) / 12))


FREQUENCIAS_NOTAS = {
    f"{nome}{oitava}": frequencia_para_tom_normalizado(f"{nome}{oitava}")
    for oitava in range(0, 9)
    for nome in NOMES_NOTAS.values()
}

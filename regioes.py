REGIOES = {
    "Norte": ["ac", "ap", "am", "pa", "ro", "rr", "to"],
    "Nordeste": ["al", "ba", "ce", "ma", "pb", "pe", "pi", "rn", "se"],
    "Centro-Oeste": ["df", "go", "ms", "mt"],
    "Sudeste": ["es", "mg", "rj", "sp"],
    "Sul": ["pr", "rs", "sc"],
}

ESTADOS = [uf for lista in REGIOES.values() for uf in lista]


def regiao_do_estado(uf):
    for regiao, lista in REGIOES.items():
        if uf in lista:
            return regiao
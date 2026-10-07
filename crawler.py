from coletor import baixar, extrair_candidatos
from regioes import ESTADOS
from banco import salvar

ELEICAO = 6257

locais = ["br"] + ESTADOS
total_novos = 0
total_pontos = 0

for uf in locais:
    try:
        endereco, dados = baixar(ELEICAO, uf)
        fichas = extrair_candidatos(ELEICAO, uf, endereco, dados)
        novos, pontos = salvar(fichas)
    except Exception as erro:
        print(uf, "| ERRO:", erro)
        continue

    total_novos += novos
    total_pontos += pontos
    print(uf, "| novos:", novos, "| pontos:", pontos)

print("TOTAL | novos:", total_novos, "| pontos:", total_pontos)
from coletor import baixar, extrair_candidatos
from banco import salvar

endereco, dados = baixar(6257, "sp")
fichas = extrair_candidatos(6257, "sp", endereco, dados)
print(salvar(fichas))
from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017")
colecao = cliente["crawler_eleicoes"]["candidatos"]


def salvar(fichas):
    novos = 0
    pontos_novos = 0

    for ficha in fichas:
        ponto = ficha.pop("ponto")
        identificacao = {
            "eleicao": ficha["eleicao"],
            "cargo": ficha["cargo"],
            "local": ficha["local"],
            "numero": ficha["numero"],
        }

        resultado = colecao.update_one(identificacao, {"$set": ficha}, upsert=True)
        if resultado.upserted_id:
            novos += 1

        resultado = colecao.update_one(
            {**identificacao, "historico.gerado_em": {"$ne": ponto["gerado_em"]}},
            {"$push": {"historico": ponto}},
        )
        pontos_novos += resultado.modified_count

    return novos, pontos_novos
import base64
import json
import requests

BASE = "https://resultados.tse.jus.br/oficial/ele2026/"


def baixar(eleicao, uf, cargo=1):
    endereco = f"{BASE}{eleicao}/dados/{uf}/{uf}-c{cargo:04d}-e{eleicao:06d}-u.jws"
    resposta = requests.get(endereco)
    resposta.raise_for_status()
    miolo = resposta.text.strip().split(".")[1]
    miolo += "=" * (-len(miolo) % 4)
    return endereco, json.loads(base64.urlsafe_b64decode(miolo))


from datetime import datetime

from regioes import regiao_do_estado


def extrair_candidatos(eleicao, uf, endereco, dados):
    cargo = dados["carg"][0]
    gerado_em = f'{dados["dg"]} {dados["hg"]}'
    fichas = []

    for agrupamento in cargo["agr"]:
        for partido in agrupamento["par"]:
            for candidato in partido["cand"]:
                fichas.append({
                    "eleicao": eleicao,
                    "cargo": int(cargo["cd"]),
                    "local": uf,
                    "regiao": regiao_do_estado(uf),
                    "numero": int(candidato["n"]),
                    "nome": candidato["nmu"],
                    "partido": partido["sg"],
                    "url_origem": endereco,
                    "coletado_em": datetime.now(),
                    "ponto": {
                        "gerado_em": gerado_em,
                        "votos": int(candidato["vap"]),
                        "percentual": float(candidato["pvap"].replace(",", ".")),
                    },
                })
    return fichas
import base64
import json
import requests

URL = "https://resultados.tse.jus.br/oficial/ele2026/6257/dados/br/br-c0001-e006257-u.jws"

resposta = requests.get(URL)
resposta.raise_for_status()

miolo = resposta.text.strip().split(".")[1]
miolo += "=" * (-len(miolo) % 4)
dados = json.loads(base64.urlsafe_b64decode(miolo))

print(dados["ele"], dados["dg"], dados["hg"])

for agrupamento in dados["carg"][0]["agr"]:
    for partido in agrupamento["par"]:
        for candidato in partido["cand"]:
            votos = int(candidato["vap"])
            percentual = float(candidato["pvap"].replace(",", "."))
            print(candidato["nmu"], "|", votos, "|", percentual)
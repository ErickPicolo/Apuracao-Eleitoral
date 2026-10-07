from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

app = FastAPI(title="API das Eleições 2026")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cliente = MongoClient("mongodb://localhost:27017")
colecao = cliente["crawler_eleicoes"]["candidatos"]


@app.get("/nacional")
def resumo_nacional():
    documentos = list(colecao.find({"local": "br"}, {"_id": 0}))
    if not documentos:
        documentos = list(colecao.find({"local": {"$ne": "br"}}, {"_id": 0}))

    totais = {}
    votos_totais = 0
    for doc in documentos:
        nome = doc.get("nome", "Outros")
        votos = doc["historico"][-1]["votos"] if doc.get("historico") else 0
        totais[nome] = totais.get(nome, 0) + votos
        votos_totais += votos

    resumo = []
    for nome, votos in sorted(totais.items(), key=lambda x: x[1], reverse=True):
        pct = round((votos / votos_totais * 100), 1) if votos_totais > 0 else 0
        resumo.append({"nome": nome, "votos": votos, "pct": pct})

    return {"votos_totais": votos_totais, "candidatos": resumo}


@app.get("/candidatos")
def listar_candidatos(local: str = "br"):
    filtro = {"local": local}
    documentos = colecao.find(filtro, {"_id": 0}).sort("historico.0.votos", -1)
    return list(documentos)


@app.get("/candidatos/{local}/{numero}")
def consultar_candidato(local: str, numero: int):
    documento = colecao.find_one({"local": local, "numero": numero}, {"_id": 0})
    if not documento:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return documento


@app.get("/estatisticas")
def estatisticas(local: str = "br"):
    documentos = list(colecao.find({"local": local}, {"_id": 0}))
    if not documentos:
        return {"local": local, "total_candidatos": 0, "total_votos_candidatos": 0, "lider": None}

    total = sum(d["historico"][-1]["votos"] for d in documentos if d.get("historico"))
    lider = max(documentos, key=lambda d: d["historico"][-1]["votos"] if d.get("historico") else 0)
    return {
        "local": local,
        "total_candidatos": len(documentos),
        "total_votos_candidatos": total,
        "lider": lider.get("nome"),
    }


@app.get("/regioes")
def votos_por_regiao(numero: int):
    resultado = {}
    for documento in colecao.find({"numero": numero, "regiao": {"$ne": None}}, {"_id": 0}):
        regiao = documento["regiao"]
        votos = documento["historico"][-1]["votos"] if documento.get("historico") else 0
        resultado[regiao] = resultado.get(regiao, 0) + votos
    return resultado


@app.get("/estados")
def resultado_por_estado():
    estados = {}
    for documento in colecao.find({"local": {"$ne": "br"}}, {"_id": 0}):
        uf = documento["local"].upper()
        nome = documento.get("nome", "Desconhecido")
        votos = documento["historico"][-1]["votos"] if documento.get("historico") else 0

        if uf not in estados:
            estados[uf] = {
                "uf": uf,
                "total": 0,
                "candidatos": {}
            }

        estados[uf]["total"] += votos
        estados[uf]["candidatos"][nome] = estados[uf]["candidatos"].get(nome, 0) + votos

    resultado = []
    for uf, dados in estados.items():
        total_estado = dados["total"]
        cand_ordenados = sorted(dados["candidatos"].items(), key=lambda x: x[1], reverse=True)

        candidatos_formatados = []
        for nome, qtd_votos in cand_ordenados:
            pct = round((qtd_votos / total_estado * 100), 1) if total_estado > 0 else 0
            candidatos_formatados.append({"nome": nome, "votos": qtd_votos, "pct": pct})

        lider_nome = candidatos_formatados[0]["nome"] if candidatos_formatados else ""
        lider_pct = candidatos_formatados[0]["pct"] if candidatos_formatados else 0

        resultado.append({
            "uf": uf,
            "total": total_estado,
            "lider_nome": lider_nome,
            "lider_pct": lider_pct,
            "candidatos": candidatos_formatados[:3]
        })

    return resultado


app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")
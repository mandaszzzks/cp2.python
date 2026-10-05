import threading
import time
from datetime import datetime, timedelta, timezone

import numpy as np
from flask import Flask, g, jsonify, request
from sklearn.ensemble import IsolationForest
from werkzeug.middleware.proxy_fix import ProxyFix

from db import mongo_db

JANELA, BLOQUEIO, INTERVALO, MIN_IPS, PISO_SEGUNDOS = 300, 60, 5, 5, 10

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
banco = mongo_db()
acessos, bloqueios = banco.acessos, banco.bloqueios


def agora():
    return datetime.now(timezone.utc)


def agregar():
    return list(acessos.aggregate([
        {"$match": {"timestamp": {"$gte": agora() - timedelta(seconds=JANELA)}, "status": {"$exists": True}}},
        {"$group": {
            "_id": "$ip",
            "total": {"$sum": 1},
            "erros": {"$sum": {"$cond": [{"$and": [{"$gte": ["$status", 400]}, {"$lt": ["$status", 500]}]}, 1, 0]}},
            "rotas": {"$addToSet": "$rota"},
            "inicio": {"$min": "$timestamp"},
            "fim": {"$max": "$timestamp"},
        }},
    ]))


def features(linha):
    duracao = max((linha["fim"] - linha["inicio"]).total_seconds(), PISO_SEGUNDOS)
    return [linha["total"] / duracao * 60, linha["erros"] / linha["total"], len(linha["rotas"])]


def analisar():
    linhas = agregar()
    if len(linhas) < MIN_IPS:
        return []
    X = np.array([features(l) for l in linhas])
    rotulos = IsolationForest(contamination=0.2, random_state=42).fit_predict(X)
    resultado = []
    for linha, x, rotulo in zip(linhas, X, rotulos):
        anomalo = rotulo == -1
        if anomalo:
            bloqueios.update_one({"ip": linha["_id"]},
                                 {"$set": {"ate": agora() + timedelta(seconds=BLOQUEIO)}}, upsert=True)
        resultado.append((linha["_id"], x, anomalo))
    return resultado


def vigiar():
    while True:
        analisar()
        time.sleep(INTERVALO)


@app.before_request
def registrar():
    ip = request.remote_addr
    g.acesso = acessos.insert_one(
        {"ip": ip, "rota": request.path, "metodo": request.method, "timestamp": agora()}).inserted_id
    if bloqueios.find_one({"ip": ip, "ate": {"$gt": agora()}}):
        return jsonify(erro="muitas requisições"), 429, {"Retry-After": str(BLOQUEIO)}


@app.after_request
def completar(resposta):
    acessos.update_one({"_id": g.acesso}, {"$set": {"status": resposta.status_code}})
    return resposta


@app.get("/")
def raiz():
    return jsonify(ok=True)


@app.get("/saude")
def saude():
    return jsonify(status="up")


if __name__ == "__main__":
    threading.Thread(target=vigiar, daemon=True).start()
    app.run(use_reloader=False)
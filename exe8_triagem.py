import math
from datetime import datetime, timezone

import numpy as np
from flask import Flask, jsonify, request
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from db import mongo_db

N_FEATURES = 4
AVISO = ("Acurácia omitida de propósito: com poucos ataques e muitos eventos normais, "
         "um modelo que sempre responde 'baixo' ainda teria acurácia alta e perderia todos os ataques.")

app = Flask(__name__)
previsoes = mongo_db().previsoes


def gerar_dados(n=1000, seed=42):
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < 0.2).astype(int)
    alto = y == 1
    X = np.column_stack([
        np.where(alto, rng.poisson(10, n), rng.poisson(1, n)),
        np.where(alto, rng.poisson(6, n), rng.poisson(1, n)) + 1,
        np.abs(np.where(alto, rng.normal(80000, 25000, n), rng.normal(3000, 2000, n))),
        np.where(alto, rng.integers(0, 6, n), rng.integers(7, 20, n)),
    ])
    ruido = rng.random(n) < 0.05
    return X, np.where(ruido, 1 - y, y)


def treinar():
    X, y = gerar_dados()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, min_samples_leaf=5, random_state=42).fit(X_tr, y_tr)
    pred = modelo.predict(X_te)
    metricas = {
        "precisao": round(precision_score(y_te, pred), 2),
        "recall": round(recall_score(y_te, pred), 2),
        "f1": round(f1_score(y_te, pred), 2),
        "matriz": confusion_matrix(y_te, pred).tolist(),
        "aviso": AVISO,
    }
    return modelo, metricas


MODELO, METRICAS = treinar()


def validar(corpo):
    features = corpo.get("features") if isinstance(corpo, dict) else None
    if not isinstance(features, list):
        return "campo 'features' obrigatório"
    if len(features) != N_FEATURES:
        return f"esperadas {N_FEATURES} features, recebidas {len(features)}"
    numerico = all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in features)
    return None if numerico else "features devem ser numéricas"


@app.post("/api/triagem")
def triagem():
    corpo = request.get_json(silent=True)
    erro = validar(corpo)
    if erro:
        return jsonify(erro=erro), 400
    features = corpo["features"]
    proba = MODELO.predict_proba([features])[0]
    saida = {"risco": "alto" if MODELO.classes_[proba.argmax()] == 1 else "baixo",
             "confianca": round(float(proba.max()), 2)}
    previsoes.insert_one({"entrada": features, **saida, "timestamp": datetime.now(timezone.utc)})
    return jsonify(saida)


@app.get("/api/modelo/metricas")
def metricas():
    return jsonify(METRICAS)


if __name__ == "__main__":
    app.run()
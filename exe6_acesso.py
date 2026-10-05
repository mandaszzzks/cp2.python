from contextlib import closing
from functools import wraps

from flask import Flask, jsonify, request

from db import mysql_conn

NIVEL_ADMIN = 5
ANALISTAS = [(1, "ana", "key-ana-001", 5), (2, "bruno", "key-bruno-002", 2)]
INCIDENTES = [(1, 1, "Brute force SSH", "critica"), (2, 2, "Phishing no RH", "media")]

app = Flask(__name__)


def consultar(sql, params=(), escrita=False):
    with closing(mysql_conn()) as con, closing(con.cursor(dictionary=True)) as cur:
        cur.execute(sql, params)
        if escrita:
            con.commit()
            return cur.rowcount
        return cur.fetchall()


def popular():
    with closing(mysql_conn()) as con, closing(con.cursor()) as cur:
        for tabela in ("incidentes", "analistas"):
            cur.execute(f"DROP TABLE IF EXISTS {tabela}")
        cur.execute("""CREATE TABLE analistas (id INT PRIMARY KEY, nome VARCHAR(50),
                       api_key VARCHAR(64) UNIQUE, nivel INT)""")
        cur.execute("""CREATE TABLE incidentes (id INT PRIMARY KEY, dono_id INT, titulo VARCHAR(100),
                       severidade VARCHAR(20), status VARCHAR(20) DEFAULT 'aberto',
                       FOREIGN KEY (dono_id) REFERENCES analistas(id))""")
        cur.executemany("INSERT INTO analistas VALUES (%s, %s, %s, %s)", ANALISTAS)
        cur.executemany("INSERT INTO incidentes (id, dono_id, titulo, severidade) VALUES (%s, %s, %s, %s)", INCIDENTES)
        con.commit()


def autenticado(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        chave = request.headers.get("X-API-Key", "")
        analistas = consultar("SELECT id, nivel FROM analistas WHERE api_key = %s", (chave,)) if chave else []
        if not analistas:
            return jsonify(erro="não autenticado"), 401
        return view(analistas[0], *args, **kwargs)
    return wrapper


def negar():
    return jsonify(erro="acesso negado"), 403


@app.get("/api/incidentes")
@autenticado
def listar(analista):
    return jsonify(consultar(
        "SELECT id, titulo, severidade, status FROM incidentes WHERE dono_id = %s", (analista["id"],)))


@app.get("/api/incidentes/<int:iid>")
@autenticado
def detalhe(analista, iid):
    linhas = consultar("SELECT id, dono_id, titulo, severidade, status FROM incidentes WHERE id = %s", (iid,))
    if linhas and linhas[0]["dono_id"] == analista["id"]:
        return jsonify(linhas[0])
    if not linhas and analista["nivel"] >= NIVEL_ADMIN:
        return jsonify(erro="não encontrado"), 404
    return negar()


@app.delete("/api/incidentes/<int:iid>")
@autenticado
def apagar(analista, iid):
    if analista["nivel"] < NIVEL_ADMIN:
        return negar()
    if not consultar("DELETE FROM incidentes WHERE id = %s", (iid,), escrita=True):
        return jsonify(erro="não encontrado"), 404
    return jsonify(removido=iid)


if __name__ == "__main__":
    popular()
    app.run()
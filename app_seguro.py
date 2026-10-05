import logging
import os
from contextlib import closing
from functools import wraps

import mysql.connector
from flask import Flask, jsonify, request
from markupsafe import escape
from werkzeug.exceptions import HTTPException

NIVEL_MINIMO = 5
HEADERS = {
    "Content-Security-Policy": "default-src 'self'",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
}

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def executar(sql, params=(), escrita=False):
    con = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database="seguranca",
    )
    with closing(con), closing(con.cursor(dictionary=True)) as cur:
        cur.execute(sql, params)
        if escrita:
            con.commit()
            return cur.rowcount
        return cur.fetchall()


def requer_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        chave = request.headers.get("X-API-Key", "")
        usuarios = executar("SELECT id, nivel FROM usuarios WHERE api_key = %s", (chave,)) if chave else []
        if not usuarios:
            logging.warning("acesso sem credencial válida: %s %s", request.method, request.path)
            return jsonify(erro="não autenticado"), 401
        if usuarios[0]["nivel"] < NIVEL_MINIMO:
            logging.warning("acesso negado: usuario=%s %s %s", usuarios[0]["id"], request.method, request.path)
            return jsonify(erro="acesso negado"), 403
        return view(usuarios[0], *args, **kwargs)
    return wrapper


@app.after_request
def cabecalhos(resposta):
    resposta.headers.update(HEADERS)
    return resposta


@app.errorhandler(Exception)
def erro_generico(erro):
    if isinstance(erro, HTTPException):
        return erro
    logging.exception("erro não tratado")
    return jsonify(erro="erro interno"), 500


@app.get("/api/usuarios/buscar")
def buscar():
    nome = request.args.get("nome", "")
    return jsonify(executar("SELECT id, nome FROM usuarios WHERE nome LIKE %s", (f"%{nome}%",)))


@app.get("/perfil")
def perfil():
    return f"<h1>Bem-vindo, {escape(request.args.get('u', ''))}</h1>"


@app.delete("/api/usuarios/<int:uid>")
@requer_admin
def remover(admin, uid):
    apagados = executar("DELETE FROM usuarios WHERE id = %s", (uid,), escrita=True)
    logging.info("usuario %s removido por admin %s (linhas=%s)", uid, admin["id"], apagados)
    if not apagados:
        return jsonify(erro="não encontrado"), 404
    return jsonify(removido=uid)


@app.get("/api/relatorio")
def relatorio():
    return jsonify(executar("SELECT * FROM tabela_inexistente"))


if __name__ == "__main__":
    app.run(host="127.0.0.1")
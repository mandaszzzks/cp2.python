import random
from contextlib import closing
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

from db import mysql_conn

COLUNAS = {"data": "criado_em", "sev": "severidade", "ip": "ip_origem"}
ORDEM = {"asc": "ASC", "desc": "DESC"}
TAMANHO_PADRAO, TAMANHO_MAXIMO = 20, 100
NOTA = (
    "LIMIT %s funciona porque é dado: o driver o envia como valor e a estrutura da query não muda.\n"
    "ORDER BY %s não funciona porque coluna é identificador: viraria string literal e ordenaria por constante.\n"
    "Dado se parametriza; identificador se escolhe numa lista fechada, nunca se concatena."
)

app = Flask(__name__)


def popular(total=150):
    with closing(mysql_conn()) as con, closing(con.cursor()) as cur:
        cur.execute("DROP TABLE IF EXISTS eventos")
        cur.execute("""CREATE TABLE eventos (id INT AUTO_INCREMENT PRIMARY KEY, criado_em DATETIME,
                       severidade ENUM('baixa','media','alta','critica'), ip_origem VARCHAR(15))""")
        agora = datetime.now()
        cur.executemany("INSERT INTO eventos (criado_em, severidade, ip_origem) VALUES (%s, %s, %s)", [
            (agora - timedelta(minutes=random.randint(0, 1440)),
             random.choice(["baixa", "media", "alta", "critica"]),
             f"10.0.0.{random.randint(1, 254)}")
            for _ in range(total)
        ])
        con.commit()


@app.get("/api/eventos")
def listar():
    coluna = COLUNAS.get(request.args.get("ordenar_por", "data"))
    sentido = ORDEM.get(request.args.get("ordem", "asc"))
    if not coluna or not sentido:
        return jsonify(erro="campo de ordenação inválido"), 400
    try:
        tamanho = int(request.args.get("tamanho", TAMANHO_PADRAO))
    except ValueError:
        return jsonify(erro="tamanho deve ser inteiro"), 400
    tamanho = max(1, min(tamanho, TAMANHO_MAXIMO))

    sql = f"SELECT id, criado_em, severidade, ip_origem FROM eventos ORDER BY {coluna} {sentido} LIMIT %s"
    with closing(mysql_conn()) as con, closing(con.cursor(dictionary=True)) as cur:
        cur.execute(sql, (tamanho,))
        return jsonify(cur.fetchall())


if __name__ == "__main__":
    popular()
    print(NOTA)
    app.run()
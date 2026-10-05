from datetime import datetime, timezone

import mysql.connector

from db import mongo_db, mysql_conn

NIVEL_ADMIN = 5
USUARIOS = [(1, "ana", "ana@x.com", 5), (2, "bruno", "bruno@x.com", 2), (3, "caio", "caio@x.com", 1)]
SEQUENCIA = [(1, 2, 4), (2, 3, 5), (1, 1, 9), (1, 99, 3)]


def popular(con):
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS usuarios")
    cur.execute("CREATE TABLE usuarios (id INT PRIMARY KEY, nome VARCHAR(50), email VARCHAR(100), nivel_acesso INT)")
    cur.executemany("INSERT INTO usuarios VALUES (%s, %s, %s, %s)", USUARIOS)
    con.commit()


def nivel_de(cur, uid):
    cur.execute("SELECT nivel_acesso FROM usuarios WHERE id = %s FOR UPDATE", (uid,))
    return cur.fetchone()


def motivo_recusa(admin, alvo, admin_id, alvo_id, novo_nivel):
    if admin is None or admin[0] < NIVEL_ADMIN:
        return "admin sem privilégio"
    if admin_id == alvo_id:
        return "auto-promoção"
    if alvo is None:
        return "alvo inexistente"
    if not isinstance(novo_nivel, int) or not 0 <= novo_nivel <= 10:
        return "nível inválido"
    return None


def alterar_nivel(con, auditoria, admin_id, alvo_id, novo_nivel):
    cur = con.cursor()
    anterior, motivo, resultado = None, None, "ERRO"
    try:
        con.start_transaction()
        admin, alvo = nivel_de(cur, admin_id), nivel_de(cur, alvo_id)
        anterior = alvo[0] if alvo else None
        motivo = motivo_recusa(admin, alvo, admin_id, alvo_id, novo_nivel)
        if motivo:
            con.rollback()
            resultado = "RECUSADO"
        else:
            cur.execute("UPDATE usuarios SET nivel_acesso = %s WHERE id = %s", (novo_nivel, alvo_id))
            con.commit()
            resultado = "OK"
    except mysql.connector.Error as erro:
        con.rollback()
        motivo = type(erro).__name__
    finally:
        auditoria.insert_one({"quem": admin_id, "alvo": alvo_id, "nivel_anterior": anterior,
                              "nivel_novo": novo_nivel, "resultado": resultado, "motivo": motivo,
                              "timestamp": datetime.now(timezone.utc)})
    return resultado, motivo


if __name__ == "__main__":
    con = mysql_conn()
    popular(con)
    auditoria = mongo_db().auditoria
    auditoria.drop()

    for admin_id, alvo_id, nivel in SEQUENCIA:
        resultado, motivo = alterar_nivel(con, auditoria, admin_id, alvo_id, nivel)
        detalhe = f" ({motivo})" if motivo else ""
        print(f"alterar_nivel({admin_id}, {alvo_id}, {nivel}) -> {resultado}{detalhe}")

    cur = con.cursor()
    cur.execute("SELECT nome, nivel_acesso FROM usuarios ORDER BY id")
    print("Níveis finais:", dict(cur.fetchall()))
    total = auditoria.count_documents({})
    recusas = auditoria.count_documents({"resultado": "RECUSADO"})
    print(f"Trilha de auditoria ao final: {total} documentos ({total - recusas} sucesso, {recusas} recusas)")
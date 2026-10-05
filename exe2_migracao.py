from collections import Counter

from db import mongo_db, mysql_conn

ATIVOS = [(1, "SRV-WEB01", "192.168.1.10", "alta"), (2, "PC-RH03", "192.168.1.45", "baixa")]
ALERTAS = [(1, 1, "BRUTE_FORCE", "critica"), (2, 1, "PORT_SCAN", "alta"), (3, 2, "XSS", "media")]

SQL_JOIN = """SELECT l.tipo, l.severidade, a.nome, a.ip, a.criticidade
              FROM alertas l JOIN ativos a ON a.id = l.ativo_id
              WHERE a.criticidade IN (%s, %s, %s) ORDER BY l.id"""


def popular(con):
    cur = con.cursor()
    for tabela in ("alertas", "ativos"):
        cur.execute(f"DROP TABLE IF EXISTS {tabela}")
    cur.execute("""CREATE TABLE ativos (id INT PRIMARY KEY, nome VARCHAR(50), ip VARCHAR(15) UNIQUE,
                   criticidade ENUM('baixa','media','alta'))""")
    cur.execute("""CREATE TABLE alertas (id INT PRIMARY KEY, ativo_id INT, tipo VARCHAR(30), severidade VARCHAR(20),
                   criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (ativo_id) REFERENCES ativos(id))""")
    cur.executemany("INSERT INTO ativos VALUES (%s, %s, %s, %s)", ATIVOS)
    cur.executemany("INSERT INTO alertas (id, ativo_id, tipo, severidade) VALUES (%s, %s, %s, %s)", ALERTAS)
    con.commit()


def como_documento(linha):
    return {"tipo": linha["tipo"], "severidade": linha["severidade"],
            "ativo": {"nome": linha["nome"], "ip": linha["ip"], "criticidade": linha["criticidade"]}}


def assinatura(tipo, severidade, ip):
    return (tipo, severidade, ip)


con = mysql_conn()
popular(con)
cur = con.cursor(dictionary=True)
cur.execute(SQL_JOIN, ("baixa", "media", "alta"))
linhas = cur.fetchall()
cur.execute("SELECT COUNT(*) AS n FROM alertas")
total_mysql = cur.fetchone()["n"]

alertas = mongo_db().alertas
alertas.drop()
alertas.insert_many([como_documento(l) for l in linhas])

origem = Counter(assinatura(l["tipo"], l["severidade"], l["ip"]) for l in linhas)
destino = Counter(assinatura(d["tipo"], d["severidade"], d["ativo"]["ip"]) for d in alertas.find())
total_mongo = alertas.count_documents({})
integra = total_mysql == total_mongo and origem == destino

print(f"MySQL: {total_mysql} alertas | MongoDB: {total_mongo} documentos -> "
      f"{'MIGRAÇÃO ÍNTEGRA' if integra else 'MIGRAÇÃO COM PERDA'}")
altos = alertas.count_documents({"ativo.criticidade": "alta"})
print(f'Consulta sem JOIN: db.alertas.find({{"ativo.criticidade":"alta"}}) -> {altos} documentos')
print("Ganha-se leitura sem JOIN, com tudo num só documento.")
print("Perde-se normalização: renomear o ativo exige update_many em todos os alertas dele.")
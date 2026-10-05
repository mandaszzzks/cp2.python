import os

import mysql.connector

con = mysql.connector.connect(host=os.environ.get("MYSQL_HOST", "localhost"),
                              user=os.environ["MYSQL_USER"], password=os.environ["MYSQL_PASSWORD"])
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS seguranca")
cur.execute("USE seguranca")
cur.execute("DROP TABLE IF EXISTS usuarios")
cur.execute("""CREATE TABLE usuarios (id INT PRIMARY KEY, nome VARCHAR(50), senha VARCHAR(100),
               api_key VARCHAR(64) UNIQUE, nivel INT)""")
cur.executemany("INSERT INTO usuarios VALUES (%s, %s, %s, %s, %s)", [
    (1, "ana", "hash-ana", "key-ana", 5),
    (2, "bruno", "hash-bruno", "key-bruno", 2),
    (3, "caio", "hash-caio", "key-caio", 1),
])
con.commit()
print("laboratório pronto: 3 usuários")
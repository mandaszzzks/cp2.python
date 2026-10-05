import random
from datetime import datetime, timedelta, timezone

from db import mongo_db

SETE_DIAS = 7 * 24 * 3600
FUSO = "America/Sao_Paulo"

agora = datetime.now(timezone.utc)
eventos = mongo_db().eventos
eventos.drop()
eventos.create_index("timestamp", expireAfterSeconds=SETE_DIAS)
eventos.insert_many([
    {"tipo": "FALHA_LOGIN", "ip": f"10.0.0.{random.randint(1, 50)}",
     "timestamp": agora - timedelta(seconds=random.randint(0, 86399))}
    for _ in range(200)
])

por_hora = list(eventos.aggregate([
    {"$match": {"timestamp": {"$gte": agora - timedelta(hours=24)}}},
    {"$group": {"_id": {"$hour": {"date": "$timestamp", "timezone": FUSO}}, "total": {"$sum": 1}}},
    {"$sort": {"_id": 1}},
]))
pico = max(por_hora, key=lambda h: h["total"])

print("=== Falhas por hora (últimas 24h) ===")
for h in por_hora:
    print(f"{h['_id']:02d}h | {'█' * h['total']} {h['total']}{'   <- pico' if h is pico else ''}")
print(f"Hora de pico: {pico['_id']:02d}h ({pico['total']} falhas)")
print("Índice TTL ativo: eventos com mais de 7 dias serão removidos automaticamente.")
print("TTL é decisão de segurança: reter log além do necessário amplia a superfície de vazamento e a exposição legal (LGPD).")
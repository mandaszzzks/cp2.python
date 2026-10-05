import time

import requests

from exe9_ratelimit import acessos, analisar, bloqueios

BASE = "http://localhost:5000"
HOSTIL = "185.220.101.1"
NORMAIS = [f"192.168.1.{n}" for n in range(10, 15)]


def get(ip, rota):
    return requests.get(BASE + rota, headers={"X-Forwarded-For": ip}, timeout=5)


acessos.drop()
bloqueios.drop()

for ip in NORMAIS:
    codigos = [get(ip, "/").status_code for _ in range(5) if not time.sleep(0.2)]
    print(ip, codigos)

for i in range(60):
    get(HOSTIL, "/" if i % 3 == 0 else f"/inexistente{i}")

print("=== Análise de acessos ===")
for ip, (rpm, taxa, rotas), anomalo in analisar():
    veredito = "ANOMALIA -> bloqueado" if anomalo else "normal"
    print(f"{ip:<15}[{rpm:6.1f} req/min | 4xx {taxa:.2f} | {int(rotas)} rotas]  -> {veredito}")

r = get(HOSTIL, "/")
print(f"Próxima requisição de {HOSTIL} -> {r.status_code} {r.json()} Retry-After: {r.headers.get('Retry-After')}")
print("Risco: com contamination=0.2 o modelo sempre aponta cerca de 20% como anômalos, mesmo sem ataque.")
print("Falso positivo derruba usuário legítimo; regra fixa é previsível e auditável, o modelo precisa de revisão humana.")
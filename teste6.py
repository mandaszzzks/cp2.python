from exe6_acesso import app, popular

ANA, BRUNO = "key-ana-001", "key-bruno-002"
MATRIZ = [
    ("get", "/api/incidentes/1", ANA, 200),
    ("get", "/api/incidentes/1", BRUNO, 403),
    ("get", "/api/incidentes/1", None, 401),
    ("get", "/api/incidentes/1", "key-inexistente", 401),
    ("get", "/api/incidentes", BRUNO, 200),
    ("delete", "/api/incidentes/2", ANA, 200),
    ("delete", "/api/incidentes/1", BRUNO, 403),
    ("get", "/api/incidentes/999", ANA, 404),
]

popular()
cliente = app.test_client()
for metodo, url, chave, esperado in MATRIZ:
    r = getattr(cliente, metodo)(url, headers={"X-API-Key": chave} if chave else {})
    print("OK   " if r.status_code == esperado else "FALHA", f"{metodo.upper():<6}{url:<22}{str(chave):<16}",
          r.status_code, r.get_json())
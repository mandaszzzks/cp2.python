from exe5_ordenacao import app, popular

CASOS = [
    ("/api/eventos?ordenar_por=sev&ordem=desc&tamanho=5", 200, 5),
    ("/api/eventos?ordenar_por=criado_em,(SELECT+1)&ordem=asc", 400, None),
    ("/api/eventos?tamanho=abc", 400, None),
    ("/api/eventos?tamanho=100000", 200, 100),
]

popular()
cliente = app.test_client()
for url, status, quantidade in CASOS:
    r = cliente.get(url)
    corpo = r.get_json()
    ok = r.status_code == status and (quantidade is None or len(corpo) == quantidade)
    resumo = f"{len(corpo)} eventos" if r.status_code == 200 else corpo
    print("OK   " if ok else "FALHA", r.status_code, url, "->", resumo)
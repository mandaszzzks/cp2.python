from exe8_triagem import app, previsoes

CORPOS = [{"features": [12, 7, 90000, 3]}, {"features": [0, 1, 1200, 14]}, {"features": [12, 7, 90000]},
          {"features": ["12", "sete", 0, 3]}, {}]

previsoes.delete_many({})
cliente = app.test_client()
for corpo in CORPOS:
    r = cliente.post("/api/triagem", json=corpo)
    print(r.status_code, corpo, "->", r.get_json())
r = cliente.post("/api/triagem")
print(r.status_code, "(sem corpo) ->", r.get_json())
print("GET /api/modelo/metricas ->", cliente.get("/api/modelo/metricas").get_json())
print("previsoes gravadas:", previsoes.count_documents({}))
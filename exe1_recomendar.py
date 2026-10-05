CHAVES = {"schema_fixo", "precisa_acid", "escala_horizontal",
          "tolera_atraso_de_consistencia", "dado_sensivel"}

ERROS_INACEITAVEIS = {
    "A07": "aceitar credencial já revogada por uma réplica atrasada é pior que ficar fora do ar",
    "A06": "vender a mesma licença duas vezes é pior que recusar a compra",
    "A08": "auditoria divergente entre réplicas não vale como prova, então é melhor recusar a escrita",
    "A04": "vazar sessão sensível pesa mais que ler um estado levemente atrasado",
    "A09": "perder 1s de log é melhor que parar de aceitar log",
}

PERFIS = {
    "credenciais_do_SOC": dict(schema_fixo=True, precisa_acid=True, escala_horizontal=False, tolera_atraso_de_consistencia=False, dado_sensivel=True),
    "telemetria_de_sensores": dict(schema_fixo=False, precisa_acid=False, escala_horizontal=True, tolera_atraso_de_consistencia=True, dado_sensivel=False),
    "trilha_de_auditoria": dict(schema_fixo=False, precisa_acid=False, escala_horizontal=True, tolera_atraso_de_consistencia=False, dado_sensivel=True),
    "carrinho_de_licencas": dict(schema_fixo=True, precisa_acid=True, escala_horizontal=False, tolera_atraso_de_consistencia=False, dado_sensivel=False),
    "cache_de_sessoes": dict(schema_fixo=True, precisa_acid=False, escala_horizontal=True, tolera_atraso_de_consistencia=True, dado_sensivel=True),
}


def escolher_risco(p):
    if p["precisa_acid"]:
        return "A07" if p["dado_sensivel"] else "A06"
    if not p["tolera_atraso_de_consistencia"]:
        return "A08"
    return "A04" if p["dado_sensivel"] else "A09"


def recomendar(perfil):
    faltando = CHAVES - perfil.keys()
    if faltando:
        raise ValueError(f"perfil sem as chaves: {sorted(faltando)}")
    relacional = perfil["precisa_acid"] or (perfil["schema_fixo"] and not perfil["escala_horizontal"])
    banco = "MySQL" if relacional else "MongoDB"
    ap = perfil["tolera_atraso_de_consistencia"] and not perfil["precisa_acid"]
    cap = "AP" if ap else "CP"
    risco = escolher_risco(perfil)
    return {"banco": banco, "cap": cap, "risco_owasp": risco,
            "justificativa": f"escolher {banco} com {cap} porque {ERROS_INACEITAVEIS[risco]}"}


if __name__ == "__main__":
    for nome, perfil in PERFIS.items():
        r = recomendar(perfil)
        print(f"{nome:<24}-> {r['banco']:<8}| {r['cap']} | {r['risco_owasp']} | {r['justificativa']}")
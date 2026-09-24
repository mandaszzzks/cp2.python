logs = [
    "[2025-02-20 08:15:01] [INFO] Login ok - IP: 192.168.1.10",
    "[2025-02-20 08:15:03] [WARNING] Area restrita - IP: 10.0.0.5",
    "[2025-02-20 08:15:10] [ERROR] Falha auth - IP: 185.220.101.1",
    "[2025-02-20 08:15:15] [INFO] Arquivo acessado - IP: 192.168.1.10",
    "[2025-02-20 08:15:22] [ERROR] Conexao recusada - IP: 185.220.101.1",
    "[2025-02-20 08:15:30] [WARNING] Certificado SSL - IP: 172.16.0.3",
    "[2025-02-20 08:15:35] [ERROR] Falha auth - IP: 10.0.0.5",
    "log malformado sem formato correto",
    "[2025-02-20 08:15:45] [ERROR] Timeout - IP: 185.220.101.1",
    "[2025-02-20 08:15:50] [WARNING] CPU alta - IP: 192.168.1.20",
    "[2025-02-20 08:16:01] [ERROR] Falha auth - IP: 185.220.101.1",
    "[2025-02-20 08:16:05] [INFO] Firewall ok - IP: 192.168.1.10",
]

niveis = {"INFO": 0, "WARNING": 0, "ERROR": 0}
erros_por_ip = {}
malformados = 0

for log in logs:
    try:
        nivel = log.split("] [")[1].split("]")[0]
        ip = log.split("IP: ")[1]
        niveis[nivel] += 1
        if nivel == "ERROR":
            erros_por_ip[ip] = erros_por_ip.get(ip, 0) + 1
    except (IndexError, KeyError):
        malformados += 1

print("=== relatorio de Logs ===")
print(f"INFO:    {niveis['INFO']} eventos")
print(f"WARNING: {niveis['WARNING']} eventos")
print(f"ERROR:   {niveis['ERROR']} eventos")
print(f"Logs malformados: {malformados}")

ip_top = max(erros_por_ip, key=erros_por_ip.get)
print(f"\nIP com mais erros: {ip_top} ({erros_por_ip[ip_top]} erros)")

print("\ndetalhamento de erros:")
for ip, qtd in erros_por_ip.items():
    palavra = "erro" if qtd == 1 else "erros"
    print(f"  {ip} → {qtd} {palavra}")


##Revisado com IA
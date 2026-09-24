acessos = {"192.168.1.10", "10.0.0.5", "185.220.101.1", "172.16.0.3",
           "192.168.1.20", "91.240.118.172", "10.0.0.12", "45.33.32.156"}

blacklist = {"185.220.101.1", "45.33.32.156", "91.240.118.172",
             "23.94.5.100", "104.244.72.115"}

maliciosos = acessos & blacklist
seguros = acessos - blacklist
nao_detectados = blacklist - acessos
total = acessos | blacklist

print("=== Relatório de Segurança ===")
print(f"IPs maliciosos detectados ({len(maliciosos)}):")
for ip in maliciosos:
    print(f"  - {ip}")

print(f"\nIPs seguros ({len(seguros)}):")
for ip in seguros:
    print(f"  - {ip}")

print(f"\nIPs da blacklist não detectados ({len(nao_detectados)}):")
for ip in nao_detectados:
    print(f"  - {ip}")

print(f"\ntotal de IPs únicos: {len(total)}")
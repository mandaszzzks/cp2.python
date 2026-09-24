ativos = [
    {"nome": "SRV-WEB01", "tipo": "servidor", "ip": "192.168.1.10", "status": "ativo"},
    {"nome": "PC-RH03", "tipo": "estacao", "ip": "192.168.1.45", "status": "ativo"},
    {"nome": "SW-CORE01", "tipo": "switch", "ip": "192.168.1.1", "status": "inativo"},
]

while True:
    print("\n[1] Cadastrar ativo\n[2] Listar ativos\n[3] Buscar por IP\n[4] Alterar status\n[5] Remover ativo\n[6] Sair")
    opcao = input("Escolha: ")

    try:
        if opcao == "1":
            nome = input("Nome: ")
            tipo = input("Tipo: ")
            ip = input("IP: ")
            for ativo in ativos:
                if ativo["ip"] == ip:
                    raise ValueError("IP já cadastrado")
            ativos.append({"nome": nome, "tipo": tipo, "ip": ip, "status": "ativo"})
            print("Cadastrado")

        elif opcao == "2":
            for ativo in ativos:
                print(ativo)

        elif opcao == "3":
            ip = input("IP: ")
            encontrado = None
            for ativo in ativos:
                if ativo["ip"] == ip:
                    encontrado = ativo
                    break
            print(encontrado if encontrado else "ativo não encontrado")

        elif opcao == "4":
            ip = input("IP: ")
            novo_status = input("novo status: ")
            for ativo in ativos:
                if ativo["ip"] == ip:
                    ativo["status"] = novo_status
                    print("status atualizado")
                    break
            else:
                print("ativo não encontrado")

        elif opcao == "5":
            ip = input("IP: ")
            for ativo in ativos:
                if ativo["ip"] == ip:
                    ativos.remove(ativo)
                    print("ativo removido")
                    break
            else:
                print("ativo não encontrado")

        elif opcao == "6":
            break

    except ValueError as e:
        print(f"Erro: {e}")



##Feito com auxilio de ia
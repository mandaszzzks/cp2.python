ips = ["192.168.1.1", "10.0.0.5", "172.16.0.3"]

while True:
    print("\n1 Adicionar IP\n2 Remover IP\n3 Listar todos\n4 Buscar IP\n5 Sair")
    opcao = input("escolha: ")

    if opcao == "1":
        ip = input("IP: ")
        if ip in ips:
            print("IP já existe na lista")
        else:
            ips.append(ip)
            print("IP adicionado")

    elif opcao == "2":
        ip = input("IP: ")
        if ip in ips:
            ips.remove(ip)
            print("IP removido")
        else:
            print("IP não encontrado")

    elif opcao == "3":
        for i, ip in enumerate(ips, 1):
            print(f"{i} - {ip}")

    elif opcao == "4":
        ip = input("IP: ")
        if ip in ips:
            print(f"IP encontrado na posição {ips.index(ip) + 1}")
        else:
            print("IP não encontrado")

    elif opcao == "5":
        print("Encerrando...........")
        break
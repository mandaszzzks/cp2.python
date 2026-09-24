import random

senhas = {
    "gmail": "MinhaS3nha!",
    "github": "Dev@2024Seguro",
    "banco_dados": "db123",
}

especiais = "!@#$%&*"
caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*"


def forca(senha):
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_especial = any(c in especiais for c in senha)

    if len(senha) < 8:
        return "fraca"
    if tem_maiuscula and tem_minuscula and tem_numero and tem_especial:
        return "forte"
    if tem_numero:
        return "media"
    return "fraca"


while True:
    print("\n[1] Cadastrar senha\n[2] Listar serviços\n[3] Buscar senha\n[4] Gerar senha aleatória\n[5] Avaliar força de todas\n[6] Exportar relatório\n[7] Sair")
    opcao = input("escolha umas das opções: ")

    if opcao == "1":
        servico = input("serviço: ")
        if servico in senhas:
            print("erro: serviço já cadastrado")
        else:
            senha = input("Senha: ")
            senhas[servico] = senha
            print(f"cadastrado, fforça: {forca(senha)}")

    elif opcao == "2":
        for servico in senhas:
            print(servico)

    elif opcao == "3":
        servico = input("serviço: ")
        print(senhas[servico] if servico in senhas else "serviço não encontrado")

    elif opcao == "4":
        tamanho = int(input("tamanho: "))
        gerada = ""
        for _ in range(tamanho):
            gerada += random.choice(caracteres)
        print(f"senha gerada: {gerada}")

    elif opcao == "5":
        for servico, senha in senhas.items():
            print(f"{servico}: {forca(senha)}")

    elif opcao == "6":
        try:
            with open("senhas_relatorio.txt", "w") as f:
                for servico, senha in senhas.items():
                    f.write(f"{servico}: {forca(senha)}\n")
            print("relatório exportado com sucesso")
        except OSError as e:
            print(f"erro ao exportar: {e}")

    elif opcao == "7":
        print("encerrando......")
        break
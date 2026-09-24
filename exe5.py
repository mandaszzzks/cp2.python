texto = input("digite um textinho: ").lower()
palavras = texto.split()
contagem = {}

for p in palavras:
    contagem[p] = contagem.get(p, 0) + 1

ordenado = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

print("=== Contagem de Palavras ===")
for palavra, qtd in ordenado:
    vez = "vez" if qtd == 1 else "vezes"
    print(f'"{palavra}" → {qtd} {vez}')

mais_frequente = ordenado[0]
print(f'\npalavra mais frequente: "{mais_frequente[0]}" ({mais_frequente[1]} vezes)')
print(f"total de palavras únicas: {len(contagem)}")
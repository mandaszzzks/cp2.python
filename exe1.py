frase = input("Digite uma frase: ")
vogais = 0
consoantes = 0

for c in frase.lower():
    if c.isalpha():
        if c in "aeiou":
            vogais += 1
        else:
            consoantes += 1

print(f'Frase: "{frase}"')
print(f"Vogais: {vogais}")
print(f"Consoantes: {consoantes}")
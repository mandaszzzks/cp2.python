alunos = [
    ("Carlos", 8.5),
    ("Ana", 9.2),
    ("Bruno", 6.0),
    ("Diana", 7.8),
    ("Eduardo", 4.5),
]

maior = alunos[0]
menor = alunos[0]
soma = 0

for nome, nota in alunos:
    if nota > maior[1]:
        maior = (nome, nota)
    if nota < menor[1]:
        menor = (nome, nota)
    soma += nota

media = soma / len(alunos)

print("=== Relatório de Notas ===")
print(f"Maior nota: {maior[0]} - {maior[1]}")
print(f"Menor nota: {menor[0]} - {menor[1]}")
print(f"Média da turma: {media:.1f}")
print("\nAlunos acima da média:")
for nome, nota in alunos:
    if nota > media:
        print(f"- {nome}: {nota}")
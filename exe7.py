while True:
    n1 = input("número 1: ")
    if n1.lower() == "sair":
        print("encerrando calculadora.")
        break

    try:
        num1 = float(n1)
        n2 = input("número 2: ")
        num2 = float(n2)
        op = input("operação: ")
        if op == "+":
            resultado = num1 + num2
        elif op == "-":
            resultado = num1 - num2
        elif op == "*":
            resultado = num1 * num2
        elif op == "/":
            resultado = num1 / num2
        else:
            raise ValueError(f"Operação '{op}' nao suportada. Use +, -, * ou /")
    except ValueError as e:
        if str(e) and "não suportada" in str(e):
            print(f"Erro: {e}")
        else:
            print("Erro: Digite apenas números")
    except ZeroDivisionError:
        print("erro: Divisão por zero nao é aceito")
    else:
        print(f"resultado: {resultado:.2f}")
    finally:
        print("Operação processada.")
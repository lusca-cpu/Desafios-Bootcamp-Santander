menu = """
    1- Depositar
    2- Sacar
    3- Extrato
    0- Sair 
"""

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        print("Depósito")
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    elif opcao == "2":
        print("Saque")
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo:
            print("Saldo insuficiente para saque.")
        
        else:
            if valor < limite:
                if LIMITE_SAQUES == numero_saques:
                    print("Número máximo de saques atingido.")
                else:
                    if saldo >= valor: 
                        numero_saques += 1
                        saldo -= valor
                        extrato.append(f"Saque: R$ {valor:.2f}")
                        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

            elif valor > limite:
                print(f"Valor do saque excede o limite de R$ {limite:.2f}.")

    elif opcao == "3":
        print("Extrato:")
        for item in extrato:
            print("- " + item)

        print(f"\nSaldo: R$ {saldo:.2f}")

    elif opcao == "0":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        continue

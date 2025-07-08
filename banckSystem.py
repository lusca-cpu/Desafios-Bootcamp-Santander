def criar_usuario(nome, cpf, data_nascimento, endereco):
    conta = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "conta_corrente": [],
    }
    return conta

def criar_conta_corrente(usuario, saldo=0, extrato=None):
    if extrato is None:
        extrato = []

    conta_corrente = {
        "num_conta": len(usuario['conta_corrente']) + 1,
        "agencia": "0001",
        "saldo": saldo,
        "extrato": extrato,
    }

    usuario['conta_corrente'].append(conta_corrente)
    return conta_corrente

def depositar(valor, saldo, extrato):
    saldo += valor
    extrato.append(f"Depósito: R$ {valor:.2f}")

    return valor, saldo

def sacar(valor, saldo, extrato, numero_saques):
    numero_saques += 1
    saldo -= valor
    extrato.append(f"Saque: R$ {valor:.2f}")

    return valor, saldo, numero_saques

def exibir_extrato(extrato, saldo):
    for item in extrato:
        print("- " + item)

    print(f"\nSaldo: R$ {saldo:.2f}")

if __name__ == "__main__":
    print("Bem-vindo ao sistema bancário!")

    usuario = []

    while True:
        print("\nDeseja criar uma conta ou acessar uma conta existente?\n" \
                "1- Criar conta\n" \
                "2- Acessar conta existente\n" \
                "0- Sair")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            print("\nCriar Conta")
            print("Informe os dados do usuário")

            nome = input("Informe o nome: ")
            cpf = input("Informe o CPF: ")
            if cpf in [usuario['cpf'] for usuario in usuario]:
                print("Já existe uma conta cadastrada com esse CPF.")
                exit()
            data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
            endereco = input("Informe o endereço: ")

            novo_usuario = criar_usuario(nome, cpf, data_nascimento, endereco)
            usuario.append(novo_usuario)
            print(f"Conta criada com sucesso para {novo_usuario['nome']}!")

        elif opcao == "2":
            print ("Acessar Conta Existente")
            cpf = input("Informe o CPF: ")
            usuario_encontrado = next((u for u in usuario if u['cpf'] == cpf), None)
            if usuario_encontrado:
                print(f"Bem-vindo, {usuario_encontrado['nome']}!")
                while True:
                    print("\nMenu de Opções:\n" \
                            "1- Acessar conta corrente\n" \
                            "2- Criar conta corrente\n" \
                            "0- Sair")
                    opcao = input("Selecione uma opção: ")

                    if opcao == "1":
                        print("Acessando conta corrente...")
                        verificar_conta = input("Digite o número da conta corrente:")

                        if verificar_conta in [str(cc['num_conta']) for cc in usuario_encontrado['conta_corrente']]:

                            usuario_encontrado = next(cc for cc in usuario_encontrado['conta_corrente'] if str(cc['num_conta']) == verificar_conta)
                            print(f"Conta corrente {usuario_encontrado['num_conta']} acessada com sucesso!")
                            menu = """
                                1- Depositar
                                2- Sacar
                                3- Extrato
                                0- Sair 
                            """
                            
                            LIMITE_SAQUES = 3
                            limite = 500
                            numero_saques = 0

                            while True:

                                opcao = input(menu)

                                if opcao == "1":
                                    print("Depósito")
                                    valor = float(input("Informe o valor do depósito: "))

                                    if valor > 0:
                                        deposito, usuario_encontrado["saldo"] = depositar(valor, usuario_encontrado["saldo"], usuario_encontrado["extrato"])
                                        print(f"Depósito de R$ {deposito:.2f} realizado com sucesso!")               
                                    else:
                                        print("Valor inválido para depósito.")

                                elif opcao == "2":
                                    
                                    print("Saque")
                                    valor = float(input("Informe o valor do saque: "))

                                    if valor > usuario_encontrado["saldo"]:
                                        print("Saldo insuficiente para saque.")
                                    
                                    else:
                                        if valor < limite:
                                            if LIMITE_SAQUES == numero_saques:
                                                print("Número máximo de saques atingido.")
                                            else:
                                                if usuario_encontrado["saldo"] >= valor: 
                                                    saque, usuario_encontrado["saldo"], numero_saques = sacar(valor, usuario_encontrado["saldo"], usuario_encontrado["extrato"], numero_saques)
                                                    print(f"Saque de R$ {saque:.2f} realizado com sucesso!")

                                        elif valor > limite:
                                            print(f"Valor do saque excede o limite de R$ {limite:.2f}.")

                                elif opcao == "3":
                                    print("Extrato:")
                                    exibir_extrato(usuario_encontrado["extrato"], usuario_encontrado["saldo"])

                                elif opcao == "0":
                                    print("Saindo do sistema. Até logo!")
                                    break

                                else:
                                    print("Operação inválida, por favor selecione novamente a operação desejada.")
                                    continue
                            break
                        
                        else:
                            print("Conta corrente não encontrada. Por favor, verifique o número da conta.")
                            continue

                    elif opcao == "2":
                        print("Criando conta corrente...")
                        criar_conta_corrente(usuario_encontrado)
                        continue

                    elif opcao == "0":
                        print("Saindo do sistema. Até logo!")
                        exit()

                    else:
                        print("Opção inválida. Por favor, selecione novamente.")

        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            exit()

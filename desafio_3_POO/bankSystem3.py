import classBankSystem as bank

def criar_usuario(usuario):
    try:
        print("Informe os dados do usuário")

        nome = input("Informe o nome: ")
        cpf = input("Informe o CPF: ")
        if usuario:
            print("Já existe uma conta cadastrada com esse CPF.")
            exit()
        data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
        endereco = input("Informe o endereço: ")

        conta = bank.PessoaFisica(nome, cpf, data_nascimento, endereco)
        usuario.append(conta)
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False

def criar_conta_corrente(usuario, contas):
    try:
        numero_conta = len(contas) + 1

        conta = bank.ContaCorrente.nova_conta(usuario, numero_conta)
        contas.append(conta)
        usuario.contas.append(conta)
        return True
    except Exception as e:
        print(f"Erro ao criar conta corrente: {e}")
        return False

def depositar(valor, conta):
    try:
        transacao = bank.Deposito(valor)
        conta.cliente.realizar_transacao(conta, transacao)
        return True
    except Exception as e:
        print(f"Erro ao realizar depósito: {e}")
        return False

def sacar(valor, conta):
    try:
        transacao = bank.Saque(valor)
        conta.cliente.realizar_transacao(conta, transacao)
        return True
    except Exception as e:
        print(f"Erro ao realizar saque: {e}")
        return False

def exibir_extrato(conta):
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Nenhuma transação realizada.")
    else:
        print("========== EXTRATO ==========")
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
        print("=============================")

if __name__ == "__main__":
    print("Bem-vindo ao sistema bancário!")

    usuario = []
    contas = []

    while True:
        print("\nDeseja criar uma conta ou acessar uma conta existente?\n" \
                "1- Criar conta\n" \
                "2- Acessar conta existente\n" \
                "0- Sair")
        opcao = input("Selecione uma opção: ")

        if opcao == "1":
            print("\nCriar Conta")
            
            if criar_usuario(usuario):
                print("Usuário criado com sucesso!")

        elif opcao == "2":
            print ("Acessar Conta Existente")
            
            cpf = input("Informe o CPF: ")
            usuario_encontrado = next((filter(lambda u: u.cpf == cpf, usuario)), None)

            if usuario_encontrado:
                print(f"Bem-vindo, {usuario_encontrado.nome}!")
                while True:
                    print("\nMenu de Opções:\n" \
                            "1- Acessar conta corrente\n" \
                            "2- Criar conta corrente\n" \
                            "0- Sair")
                    opcao = input("Selecione uma opção: ")

                    if opcao == "1":
                        print("Acessando conta corrente...")
                        numero_conta = input("Digite o número da conta corrente: ")

                        if numero_conta.isdigit():
                            numero_conta = int(numero_conta)
                            contas_usuario = usuario_encontrado.contas
                            if numero_conta in [cc.numero for cc in contas_usuario]:
                                conta_encontrada = next(cc for cc in contas_usuario if cc.numero == numero_conta)

                                print(f"Conta corrente {conta_encontrada.numero} acessada com sucesso!")
                                menu = """
                                    1- Depositar
                                    2- Sacar
                                    3- Extrato
                                    0- Sair 
                                """

                                while True:

                                    opcao = input(menu)

                                    if opcao == "1":
                                        print("Depósito")
                                        valor = float(input("Informe o valor do depósito: "))

                                        if depositar(valor, conta_encontrada):
                                            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")               
                                        else:
                                            print("Valor inválido para depósito.")

                                    elif opcao == "2": 
                                        print("Saque")
                                        valor = float(input("Informe o valor do saque: "))

                                        if valor > conta_encontrada.saldo:
                                            print("Saldo insuficiente para saque.")
                                        
                                        else:
                                            if sacar(valor, conta_encontrada):
                                                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

                                    elif opcao == "3":
                                        exibir_extrato(conta_encontrada)

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
                        if criar_conta_corrente(usuario_encontrado, contas):
                            print("Conta corrente criada com sucesso!")
                        else:
                            print("Erro ao criar conta corrente. Tente novamente.")
                        continue

                    elif opcao == "0":
                        print("Saindo do sistema. Até logo!")
                        exit()

                    else:
                        print("Opção inválida. Por favor, selecione novamente.")

        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            exit()
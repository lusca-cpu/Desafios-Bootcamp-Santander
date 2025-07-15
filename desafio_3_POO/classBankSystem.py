from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._agencia = "0001"
        self._saldo = 0
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self): 
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if valor > saldo:
            print("Saldo insuficiente para saque.")
            return False
        elif valor <= 0:
            print("Valor de saque inválido.")
            return False
        else:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            return True
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True
        else:
            print("Valor inválido para depósito.")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Número máximo de saques atingido.")
            return False
        elif excedeu_saques:
            print(f"Operação falhou! Número máximo de saques excedido.")
            return False
        else:
            return super().sacar(valor)
        
    def __str__(self):
        return f"""\
            Conta Corrente:
            Número: {self.numero()}
            Agência: {self.agencia()}
            Cliente: {self.cliente().nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self, valor):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
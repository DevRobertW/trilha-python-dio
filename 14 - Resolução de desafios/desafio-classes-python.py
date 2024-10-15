import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# Classe base que representa um cliente no sistema bancário
class Cliente:
    """Classe que representa um cliente no sistema bancário."""

    def __init__(self, endereco: str):
        self.endereco: str = endereco  # Endereço do cliente
        self.contas: List['Conta'] = []  # Lista de contas associadas ao cliente

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        """Realiza uma transação em uma conta associada."""
        transacao.registrar(conta)  # Executa a transação na conta especificada

    def adicionar_conta(self, conta: 'Conta'):
        """Adiciona uma conta ao cliente."""
        self.contas.append(conta)  # Adiciona a conta à lista de contas do cliente

# Classe que representa um cliente pessoa física, herda de Cliente
class PessoaFisica(Cliente):
    """Classe que representa um cliente pessoa física."""

    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)  # Inicializa o endereço na classe pai
        self.nome: str = nome  # Nome completo do cliente
        self.data_nascimento: str = data_nascimento  # Data de nascimento do cliente
        self.cpf: str = cpf  # CPF do cliente

# Classe que representa uma conta bancária genérica
class Conta:
    """Classe que representa uma conta bancária genérica."""

    def __init__(self, numero: int, cliente: Cliente):
        self._saldo: float = 0.0  # Saldo inicial da conta
        self._numero: int = numero  # Número da conta
        self._agencia: str = "0001"  # Agência padrão
        self._cliente: Cliente = cliente  # Cliente associado à conta
        self._historico: Historico = Historico()  # Histórico de transações da conta

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        """Cria uma nova conta para um cliente."""
        return cls(numero, cliente)  # Retorna uma nova instância de Conta

    @property
    def saldo(self) -> float:
        return self._saldo  # Retorna o saldo atual da conta

    @property
    def numero(self) -> int:
        return self._numero  # Retorna o número da conta

    @property
    def agencia(self) -> str:
        return self._agencia  # Retorna a agência da conta

    @property
    def cliente(self) -> Cliente:
        return self._cliente  # Retorna o cliente associado à conta

    @property
    def historico(self) -> 'Historico':
        return self._historico  # Retorna o histórico de transações

    def sacar(self, valor: float) -> bool:
        """Realiza saque na conta, se possível."""
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False  # Não permite sacar valores negativos ou zero

        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False  # Verifica se há saldo suficiente para o saque

        self._saldo -= valor  # Deduz o valor do saque do saldo
        print("\n=== Saque realizado com sucesso! ===")
        return True  # Saque realizado com sucesso

    def depositar(self, valor: float) -> bool:
        """Realiza um depósito na conta."""
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False  # Não permite depositar valores negativos ou zero

        self._saldo += valor  # Adiciona o valor do depósito ao saldo
        print("\n=== Depósito realizado com sucesso! ===")
        return True  # Depósito realizado com sucesso

# Classe que representa uma conta corrente, herda de Conta
class ContaCorrente(Conta):
    """Classe que representa uma conta corrente com limite de saque e número de saques."""

    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)  # Inicializa atributos da classe pai
        self._limite: float = limite  # Limite máximo por saque
        self._limite_saques: int = limite_saques  # Número máximo de saques por dia

    def sacar(self, valor: float) -> bool:
        """Realiza saque respeitando limite de valor e número de saques."""
        # Calcula o número de saques já realizados
        saques_realizados = sum(
            1 for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__
        )

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False  # Impede saques acima do limite

        if saques_realizados >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False  # Impede exceder o número máximo de saques

        return super().sacar(valor)  # Realiza o saque usando o método da classe pai

    def __str__(self) -> str:
        """Retorna uma string representando a conta corrente."""
        return f"Agência: {self.agencia}\nC/C: {self.numero}\nTitular: {self.cliente.nome}"

# Classe que armazena o histórico de transações de uma conta
class Historico:
    """Classe que armazena o histórico de transações de uma conta."""

    def __init__(self):
        self._transacoes: List[dict] = []  # Lista de transações

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes  # Retorna a lista de transações

    def adicionar_transacao(self, transacao: 'Transacao'):
        """Adiciona uma nova transação ao histórico."""
        # Adiciona um dicionário com detalhes da transação
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,  # Tipo de transação (Saque ou Deposito)
            "valor": transacao.valor,  # Valor da transação
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  # Data e hora da transação
        })

# Classe abstrata que representa uma transação
class Transacao(ABC):
    """Classe abstrata que representa uma transação."""

    @property
    @abstractmethod
    def valor(self) -> float:
        pass  # Método abstrato para obter o valor da transação

    @abstractmethod
    def registrar(self, conta: Conta):
        pass  # Método abstrato para registrar a transação em uma conta

# Classe que representa uma transação de saque, herda de Transacao
class Saque(Transacao):
    """Classe que representa uma transação de saque."""

    def __init__(self, valor: float):
        self._valor = valor  # Valor do saque

    @property
    def valor(self) -> float:
        return self._valor  # Retorna o valor do saque

    def registrar(self, conta: Conta):
        """Registra um saque na conta."""
        if conta.sacar(self.valor):  # Tenta realizar o saque na conta
            conta.historico.adicionar_transacao(self)  # Adiciona ao histórico se bem-sucedido

# Classe que representa uma transação de depósito, herda de Transacao
class Deposito(Transacao):
    """Classe que representa uma transação de depósito."""

    def __init__(self, valor: float):
        self._valor = valor  # Valor do depósito

    @property
    def valor(self) -> float:
        return self._valor  # Retorna o valor do depósito

    def registrar(self, conta: Conta):
        """Registra um depósito na conta."""
        if conta.depositar(self.valor):  # Tenta realizar o depósito na conta
            conta.historico.adicionar_transacao(self)  # Adiciona ao histórico se bem-sucedido

# Função para exibir o menu e obter a opção do usuário
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para filtrar um cliente pelo CPF
def filtrar_cliente(cpf: str, clientes: List[Cliente]) -> Optional[Cliente]:
    """Busca um cliente pelo CPF."""
    # Retorna o primeiro cliente encontrado com o CPF correspondente, ou None se não encontrar
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente: Cliente) -> Optional[Conta]:
    """Recupera a conta do cliente, ou exibe uma mensagem se ele não tiver conta."""
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None  # Retorna None se o cliente não tiver contas
    return cliente.contas[0]  # Retorna a primeira conta do cliente

# Função para realizar um depósito
def depositar(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  # Busca o cliente pelo CPF
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)  # Cria uma transação de depósito
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)  # Realiza a transação na conta
    except ValueError:
        print("\n@@@ Valor inválido! @@@")  # Trata entrada inválida

# Função para realizar um saque
def sacar(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  # Busca o cliente pelo CPF
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)  # Cria uma transação de saque
        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao)  # Realiza a transação na conta
    except ValueError:
        print("\n@@@ Valor inválido! @@@")  # Trata entrada inválida

# Função para exibir o extrato de um cliente
def exibir_extrato(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  # Busca o cliente pelo CPF

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")  # Informa se não houver transações
    else:
        for transacao in transacoes:
            # Exibe cada transação com seu tipo e valor
            print(f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} em {transacao['data']}")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")  # Exibe o saldo atual da conta
    print("==========================================")

# Função para criar um novo cliente
def criar_cliente(clientes: List[Cliente]):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)  # Verifica se o cliente já existe

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    # Solicita os dados do novo cliente
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)  # Adiciona o novo cliente à lista de clientes

    print("\n=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta para um cliente existente
def criar_conta(numero_conta: int, clientes: List[Cliente], contas: List[Conta]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  # Busca o cliente pelo CPF

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)  # Cria uma nova conta corrente
    contas.append(conta)  # Adiciona a conta à lista de contas
    cliente.adicionar_conta(conta)  # Associa a conta ao cliente

    print("\n=== Conta criada com sucesso! ===")

# Função para listar todas as contas cadastradas
def listar_contas(contas: List[Conta]):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))  # Exibe as informações da conta

# Função principal que executa o sistema bancário
def main():
    clientes: List[Cliente] = []  # Lista de clientes
    contas: List[Conta] = []  # Lista de contas

    while True:
        opcao = menu()  # Exibe o menu e obtém a opção do usuário

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1  # Gera um número de conta sequencial
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário!")
            break  # Sai do loop e encerra o programa

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Inicia a execução do programa
if __name__ == "__main__":
    main()

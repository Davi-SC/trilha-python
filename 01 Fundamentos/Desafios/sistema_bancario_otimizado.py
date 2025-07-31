# Sistema Bancário Otimizado com Funções e novas operações
import textwrap

def menu():
    menu_str = """\
    ================ MENU ================
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q] \tSair
    ======================================
    => """
    return input(textwrap.dedent(menu_str))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito:\tR$ {valor:.2f}")
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque na conta.
    Argumentos nomeados obrigatórios: saldo, valor, extrato, limite, numero_saques, limite_saques.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque:\t\tR$ {valor:.2f}")
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\nOperação falhou! O valor informado é inválido. @@@")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in extrato:
            print(transacao)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\nJá existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios, contas):
    
    cpf = input("Informe o CPF do usuário (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")
        return None

    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    contas.append(conta)
    print(f"\n=== Conta {agencia}-{numero_conta} criada com sucesso para {usuario['nome']}! ===")
    return conta 

def listar_contas(contas):
    """
    Lista todas as contas cadastradas no sistema.
    """
    if not contas:
        print("\nNão há contas cadastradas.")
        return

    print("\n============== LISTA DE CONTAS ==============")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
        print("-" * 50) 
    print("==============================================")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = []  
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("\nValor inválido. Digite um número.")
                continue 
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("\nValor inválido. Digite um número. ")
                continue 
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            nova_conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nSaindo do sistema. Obrigado!")
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

main()
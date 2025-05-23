import textwrap
from datetime import datetime


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

def ler_cpf(mensagem="Informe o CPF (somente número): "):
    try:
       cpf_lido = input(mensagem)
       int(cpf_lido)
       return cpf_lido
    except ValueError:
       print("\n=== CPF inválido! ===")
       return None


def ler_valor(mensagem, valor_invalido = -1):
    try:
       return float(input(mensagem))
    except ValueError:
       return valor_invalido

def para_extrato(tipo, valor):
    agora = datetime.now() 
    return f"{tipo}:\tR$ {valor:.2f} as {agora:%c}\n"

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += para_extrato("Depósito",valor)
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += para_extrato("Saque", valor)
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = ler_cpf()
    if not cpf:
        return
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios[cpf] = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):    
    return usuarios.get(cpf)


def criar_conta(agencia, numero_conta, usuarios):
    cpf = ler_cpf("Informe o CPF do usuário: ")
    if not cpf:
        return None, None

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}, cpf

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None, None


def listar_contas(usuarios):
    for usuario in usuarios.values():
        print("=" * 100)
        print(' ... Usuario: ',usuario.get("nome"), usuario.get("cpf"))
        
        contas = usuario.get("contas")
        if contas:
            for conta in contas:
                linha = f"""\
                    Agência:\t{conta['agencia']}
                    C/C:\t\t{conta['numero_conta']}
                    Titular:\t{conta['usuario']['nome']}
                """
                print(textwrap.dedent(linha))
        else:
            print("   Nenhuma conta registrada neste CPF ")
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = {}
    numero_ultima_conta = 0

    while True:
        opcao = menu()

        if opcao == "d":
            valor = ler_valor("Informe o valor do depósito: ")

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = ler_valor("Informe o valor do saque: ")

            saldo, extrato = sacar(
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
            
            conta, cpf = criar_conta(AGENCIA, numero_ultima_conta+1, usuarios)
            if conta and cpf:
                numero_ultima_conta = numero_ultima_conta + 1
                usuario = usuarios[cpf]
                usuario.setdefault("contas",[])
                contas  = usuario["contas"] + [conta]
                usuario["contas"] = contas
                usuarios[cpf] = usuario                

        elif opcao == "lc":
            listar_contas(usuarios)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

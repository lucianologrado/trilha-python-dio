import datetime

menu = """

Seu saldo atual: {:.2f}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def para_extrato(tipo, valor):
    agora = datetime.datetime.now() 
    return f"{tipo.center(10)}: R$ {valor:.2f} as {agora:%c}\n"

def falha_operacao(mensagem):
    print(f"Operação falhou! {mensagem}.")    

def ler_valor(mensagem, valor_invalido = -1):
    try:
       return float(input(mensagem))
    except ValueError:
       return valor_invalido
            

while True:

    opcao = input(menu.format(saldo))

    

    if opcao == "d":

        valor = ler_valor("Informe o valor do depósito: ")
        if valor > 0:
            saldo += valor
            extrato += para_extrato("Depósito", valor)
        else:
            falha_operacao("O valor informado é inválido")

    elif opcao == "s":
        valor = ler_valor("Informe o valor do depósito: ")

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        
        if excedeu_saldo:
            falha_operacao("Você não tem saldo suficiente")
        elif excedeu_limite:
            falha_operacao("O valor do saque excede o limite")
        elif excedeu_saques:
            falha_operacao("Número máximo de saques excedido")
        elif valor > 0:
            saldo -= valor
            extrato += para_extrato("Saque", valor)
            numero_saques += 1
        else:
            falha_operacao("O valor informado é inválido")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

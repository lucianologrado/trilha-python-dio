from datetime import datetime

menu = """

Seu saldo atual: {:.2f}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
LIMITE_POR_SAQUE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
MENSAGEM_VALOR_INVALIDO = "O valor informado é inválido"

def para_extrato(tipo, valor):
    agora = datetime.now() 
    return f"{tipo.center(10)}: R$ {valor:.2f} as {agora:%c}\n"

def falha_operacao(mensagem):
    print(f"Operação falhou! {mensagem}.")    

def ler_valor(mensagem, valor_invalido = -1):
    try:
       return float(input(mensagem))
    except ValueError:
       return valor_invalido
    
def viola_regras_saque(saldo, valor, numero_saques):
        valor_invalido = valor <= 0
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > LIMITE_POR_SAQUE
        excedeu_saques = numero_saques >= LIMITE_SAQUES
        
        if excedeu_saldo:
            falha_operacao("Você não tem saldo suficiente")
        elif excedeu_limite:
            falha_operacao("O valor do saque excede o limite")
        elif excedeu_saques:
            falha_operacao("Número máximo de saques excedido")
        elif valor_invalido:
            falha_operacao(MENSAGEM_VALOR_INVALIDO)
        return  valor_invalido or excedeu_limite or excedeu_saldo or excedeu_saques   

            

while True:

    opcao = input(menu.format(saldo))

    

    if opcao == "d":

        valor = ler_valor("Informe o valor do depósito: ")
        if valor > 0:
            saldo += valor
            extrato += para_extrato("Depósito", valor)
        else:
            falha_operacao(MENSAGEM_VALOR_INVALIDO)

    elif opcao == "s":
        valor = ler_valor("Informe o valor do depósito: ")

        if not viola_regras_saque(saldo, valor, numero_saques):
            saldo -= valor
            extrato += para_extrato("Saque", valor)
            numero_saques += 1

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

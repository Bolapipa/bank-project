from datetime import datetime, date

def mostrar_menu():
    menu = """
💰 [d] Depositar
💸 [s] Sacar
📄 [e] Extrato
👀 [v] Visualizar saldo
❌ [q] Sair
=> """
    return input(menu)

def depositar(saldo, extrato):
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Operação falhou! Valor inválido.")
        return saldo, extrato

    if valor > 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saldo += valor
        extrato += f"{timestamp} - Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(saldo, extrato, numero_saques, limite):
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Operação falhou! Valor inválido.")
        return saldo, extrato, numero_saques

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"Operação falhou! O limite por saque é R$ {limite:.2f}.")
    elif valor > 0:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} - Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def mostrar_saldo(saldo):
    print(f"\nSeu saldo atual é: R$ {saldo:.2f}\n")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    # Novo: controle de transações diárias
    numero_transacoes_dia = 0
    data_contagem = date.today()

    while True:
        # Reset diário, se necessário
        hoje = date.today()
        if hoje != data_contagem:
            numero_transacoes_dia = 0
            data_contagem = hoje

        opcao = mostrar_menu()

        if opcao == "d":
            if numero_transacoes_dia >= 10:
                print("Operação falhou! Você excedeu o número de transações permitidas para hoje (10).")
            else:
                extrato_pre = extrato
                saldo, extrato = depositar(saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "s":
            if numero_transacoes_dia >= 10:
                print("Operação falhou! Você excedeu o número de transações permitidas para hoje (10).")
            else:
                extrato_pre = extrato
                saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques, limite)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "e":
            mostrar_extrato(saldo, extrato)

        elif opcao == "v":
            mostrar_saldo(saldo)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário! 😊")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()

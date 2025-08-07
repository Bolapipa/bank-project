from datetime import datetime, date
import pytz

# Armazena todos os usuários cadastrados
# Cada entrada é:
# cpf (str) -> {
#     "senha": str,
#     "saldo": float,
#     "extrato": str,
#     "numero_saques": int,
#     "numero_transacoes_dia": int,
#     "data_contagem": date
# }
users = {}

# Ícones para interface
ICON_LOGIN = "🔑"
ICON_EXIT = "❌"
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_INFO = "ℹ️"
ICON_CPF = "👤"
ICON_KEY = "🔒"
ICON_DEPOSIT = "💰"
ICON_WITHDRAW = "💸"
ICON_PIX = "⚡"
ICON_MENU = "✨"

# Fuso horário Brasil/São Paulo
TZ = pytz.timezone("America/Sao_Paulo")


def mostrar_menu_transacoes():
    menu = f"""
{ICON_MENU}─── Operações Bancárias ───{ICON_MENU}
{ICON_DEPOSIT} [d] Depositar
{ICON_WITHDRAW} [s] Saque
{ICON_PIX} [p] Pix
📄 [e] Extrato
👀 [v] Saldo
{ICON_EXIT} [q] Sair
🚀 Escolha: """
    return input(menu)


def autenticar(usuario):
    senha = input(f"{ICON_KEY} Digite sua senha (4 dígitos): ")
    if senha != users[usuario]["senha"]:
        print(f"{ICON_ERROR} Senha incorreta!")
        return False
    return True


def depositar(usuario, saldo, extrato):
    try:
        valor = float(input(f"{ICON_DEPOSIT} Informe o valor do depósito: R$ "))
    except ValueError:
        print(f"{ICON_ERROR} Valor inválido.")
        return saldo, extrato

    # Autenticação após informar valor
    if not autenticar(usuario):
        print(f"{ICON_ERROR} Depósito cancelado.")
        return saldo, extrato

    if valor > 0:
        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        saldo += valor
        extrato += f"{timestamp} - {ICON_DEPOSIT} Depósito: R$ {valor:.2f}\n"
        print(f"{ICON_SUCCESS} Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print(f"{ICON_ERROR} Valor inválido.")
    return saldo, extrato


def sacar(usuario, saldo, extrato, numero_saques, limite):
    try:
        valor = float(input(f"{ICON_WITHDRAW} Informe o valor do saque: R$ "))
    except ValueError:
        print(f"{ICON_ERROR} Valor inválido.")
        return saldo, extrato, numero_saques

    # Autenticação após informar valor
    if not autenticar(usuario):
        print(f"{ICON_ERROR} Saque cancelado.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print(f"{ICON_ERROR} Saldo insuficiente.")
    elif valor > limite:
        print(f"⚠️ Limite por saque: R$ {limite:.2f}.")
    elif valor > 0:
        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} - {ICON_WITHDRAW} Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"{ICON_SUCCESS} Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print(f"{ICON_ERROR} Valor inválido.")
    return saldo, extrato, numero_saques


def pix(usuario, saldo, extrato):
    destino = input(f"{ICON_CPF} CPF destinatário (11 dígitos): ")
    if not destino.isdigit():
        print(f"{ICON_ERROR} CPF inválido! Use apenas números.")
        return saldo, extrato
    if len(destino) != 11:
        print(f"{ICON_ERROR} CPF deve conter 11 dígitos.")
        return saldo, extrato
    if destino == usuario:
        print(f"{ICON_ERROR} Não é possível fazer PIX para o próprio CPF.")
        return saldo, extrato

    try:
        valor = float(input(f"{ICON_PIX} Informe o valor do PIX: R$ "))
    except ValueError:
        print(f"{ICON_ERROR} Valor inválido.")
        return saldo, extrato

    # Autenticação após informar valor
    if not autenticar(usuario):
        print(f"{ICON_ERROR} PIX cancelado.")
        return saldo, extrato

    now = datetime.now(TZ)
    # Não permitir PIX > 500 após 23:59
    if now.hour == 23 and now.minute >= 59 and valor > 500:
        print(f"{ICON_ERROR} PIX acima de R$ 500 não permitido após 23:59.")
        return saldo, extrato

    if valor > saldo:
        print(f"{ICON_ERROR} Saldo insuficiente.")
    elif valor <= 0:
        print(f"{ICON_ERROR} Valor inválido.")
    else:
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} - {ICON_PIX} PIX para {destino}: R$ {valor:.2f}\n"
        print(f"{ICON_SUCCESS} PIX de R$ {valor:.2f} enviado para {destino} com sucesso!")
    return saldo, extrato


def mostrar_extrato(saldo, extrato):
    print(f"\n{ICON_MENU}── EXTRATO ──{ICON_MENU}")
    if not extrato:
        print(f"{ICON_INFO} Sem movimentações.")
    else:
        print(extrato, end="")
    print(f"\n💳 Saldo: R$ {saldo:.2f}\n")


def registrar():
    print(f"\n🔐── Cadastro de Usuário ──🔐")
    while True:
        cpf = input(f"{ICON_CPF} CPF (11 dígitos, somente números, ex: 12345678901): ")
        if not cpf.isdigit():
            print(f"{ICON_ERROR} CPF inválido! Use apenas números.")
        elif len(cpf) != 11:
            print(f"{ICON_ERROR} CPF deve conter exatamente 11 dígitos.")
        elif cpf in users:
            print(f"{ICON_ERROR} CPF já cadastrado!")
        else:
            break

    while True:
        senha = input(f"{ICON_KEY} Crie senha (4 dígitos): ")
        if not (senha.isdigit() and len(senha) == 4):
            print(f"{ICON_ERROR} Senha inválida! Deve ter 4 dígitos.")
        else:
            break

    users[cpf] = {
        "senha": senha,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
        "numero_transacoes_dia": 0,
        "data_contagem": date.today()
    }
    print(f"{ICON_SUCCESS} Usuário cadastrado!")


def login_user():
    print(f"\n🔑── Login de Usuário ──🔑")
    cpf = input(f"{ICON_CPF} CPF: ")
    senha = input(f"{ICON_KEY} Senha: ")
    user = users.get(cpf)
    if user and user["senha"] == senha:
        print(f"{ICON_SUCCESS} Login bem-sucedido!\n")
        return cpf
    print(f"{ICON_ERROR} CPF ou senha inválidos!\n")
    return None


def main():
    # Menu inicial
    while True:
        print(f"🏦── Bem-vindo ao Sistema Bancário ──🏦")
        print(f"👥 [c] Cadastro")
        print(f"🔑 [l] Login")
        print(f"❌ [q] Sair")
        opc = input("🚀 Escolha: ").lower()

        if opc == "c":
            registrar()
        elif opc == "l":
            usuario = login_user()
            if usuario:
                break
        elif opc == "q":
            print(f"👋 Até breve!")
            return
        else:
            print(f"{ICON_ERROR} Opção inválida!\n")

    user_data = users[usuario]
    saldo = user_data["saldo"]
    extrato = user_data["extrato"]
    numero_saques = user_data["numero_saques"]
    numero_transacoes_dia = user_data["numero_transacoes_dia"]
    data_contagem = user_data["data_contagem"]
    limite = 500

    while True:
        hoje = date.today()
        if hoje != data_contagem:
            numero_transacoes_dia = 0
            data_contagem = hoje

        opcao = mostrar_menu_transacoes()

        if opcao == "d":
            if numero_transacoes_dia >= 10:
                print(f"🔥 Limite diário atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato = depositar(usuario, saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "s":
            if numero_transacoes_dia >= 10:
                print(f"🔥 Limite diário atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato, numero_saques = sacar(usuario, saldo, extrato, numero_saques, limite)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "p":
            if numero_transacoes_dia >= 10:
                print(f"🔥 Limite diário atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato = pix(usuario, saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "e":
            mostrar_extrato(saldo, extrato)

        elif opcao == "v":
            print(f"👀 Saldo: R$ {saldo:.2f}\n")

        elif opcao == "q":
            print(f"🙏 Obrigado! Até logo!")
            user_data.update({
                "saldo": saldo,
                "extrato": extrato,
                "numero_saques": numero_saques,
                "numero_transacoes_dia": numero_transacoes_dia,
                "data_contagem": data_contagem
            })
            break

        else:
            print(f"{ICON_ERROR} Operação inválida!")

        user_data.update({
            "saldo": saldo,
            "extrato": extrato,
            "numero_saques": numero_saques,
            "numero_transacoes_dia": numero_transacoes_dia,
                "data_contagem": data_contagem
            })

if __name__ == "__main__":
    main()
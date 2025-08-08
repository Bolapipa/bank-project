from datetime import datetime, date
import pytz
import json
import os
import re
from typing import Dict, Any, Optional, Tuple

# Constantes do sistema
LIMITE_SAQUE = 500.0
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACOES_DIARIAS = 10
LIMITE_PIX_NOTURNO = 500.0
HORA_LIMITE_PIX = 23
MINUTO_LIMITE_PIX = 59

# Armazena todos os usuários cadastrados
# Cada entrada é:
# cpf (str) -> {
#     "senha": str,
#     "saldo": float,
#     "extrato": str,
#     "numero_saques": int,
#     "numero_transacoes_dia": int,
#     "data_contagem": date,
#     "nome": str,
#     "email": str,
#     "telefone": str,
#     "data_cadastro": str,
#     "status": str
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
ICON_EXTRATO = "📄"
ICON_SALDO = "👀"
ICON_USER = "👨‍💼"
ICON_EMAIL = "📧"
ICON_PHONE = "📱"
ICON_SAVE = "💾"
ICON_LOAD = "📂"
ICON_SETTINGS = "⚙️"
ICON_HISTORY = "📊"
ICON_TRANSFER = "🔄"

# Fuso horário Brasil/São Paulo
TZ = pytz.timezone("America/Sao_Paulo")

# Arquivo para persistência de dados
DATA_FILE = "bank_data.json"


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo oficial brasileiro
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica se os dígitos calculados são iguais aos do CPF
    return cpf[-2:] == f"{digito1}{digito2}"


def validar_email(email: str) -> bool:
    """
    Valida formato de email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validar_telefone(telefone: str) -> bool:
    """
    Valida formato de telefone brasileiro
    """
    # Remove caracteres não numéricos
    telefone = re.sub(r'[^0-9]', '', telefone)
    # Verifica se tem 10 ou 11 dígitos (com DDD)
    return len(telefone) in [10, 11]


def salvar_dados():
    """
    Salva dados dos usuários em arquivo JSON
    """
    try:
        # Converte objetos date para string
        dados_para_salvar = {}
        for cpf, user_data in users.items():
            dados_para_salvar[cpf] = user_data.copy()
            if isinstance(user_data.get("data_contagem"), date):
                dados_para_salvar[cpf]["data_contagem"] = user_data["data_contagem"].isoformat()
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=2, ensure_ascii=False)
        print(f"{ICON_SAVE} Dados salvos com sucesso!")
    except Exception as e:
        print(f"{ICON_ERROR} Erro ao salvar dados: {e}")


def carregar_dados():
    """
    Carrega dados dos usuários do arquivo JSON
    """
    global users
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                dados_carregados = json.load(f)
            
            # Converte strings de data de volta para objetos date
            for cpf, user_data in dados_carregados.items():
                if isinstance(user_data.get("data_contagem"), str):
                    user_data["data_contagem"] = date.fromisoformat(user_data["data_contagem"])
            
            users = dados_carregados
            print(f"{ICON_LOAD} Dados carregados com sucesso!")
        except Exception as e:
            print(f"{ICON_ERROR} Erro ao carregar dados: {e}")


def mostrar_menu_transacoes():
    """
    Exibe menu de operações bancárias
    """
    menu = f"""
{ICON_MENU}─── Operações Bancárias ───{ICON_MENU}
{ICON_DEPOSIT} [d] Depositar
{ICON_WITHDRAW} [s] Saque
{ICON_PIX} [p] Pix
{ICON_TRANSFER} [t] Transferência
{ICON_EXTRATO} [e] Extrato
{ICON_SALDO} [v] Saldo
{ICON_HISTORY} [h] Histórico
{ICON_SETTINGS} [c] Configurações
{ICON_EXIT} [q] Sair
🚀 Escolha: """
    return input(menu).lower()


def autenticar(usuario: str, max_tentativas: int = 3) -> bool:
    """
    Autentica usuário com limite de tentativas
    """
    for tentativa in range(max_tentativas):
        senha = input(f"{ICON_KEY} Digite sua senha (4 dígitos): ")
        if senha == users[usuario]["senha"]:
            return True
        else:
            tentativas_restantes = max_tentativas - tentativa - 1
            if tentativas_restantes > 0:
                print(f"{ICON_ERROR} Senha incorreta! Tentativas restantes: {tentativas_restantes}")
            else:
                print(f"{ICON_ERROR} Número máximo de tentativas excedido!")
    
    return False


def depositar(usuario: str, saldo: float, extrato: str) -> Tuple[float, str]:
    """
    Realiza depósito na conta
    """
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


def sacar(usuario: str, saldo: float, extrato: str, numero_saques: int, limite: float) -> Tuple[float, str, int]:
    """
    Realiza saque da conta
    """
    # Verifica limite de saques diários
    if numero_saques >= LIMITE_SAQUES_DIARIOS:
        print(f"{ICON_ERROR} Limite de {LIMITE_SAQUES_DIARIOS} saques diários atingido!")
        return saldo, extrato, numero_saques

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


def pix(usuario: str, saldo: float, extrato: str) -> Tuple[float, str]:
    """
    Realiza transferência PIX
    """
    destino = input(f"{ICON_CPF} CPF destinatário (11 dígitos): ")
    if not destino.isdigit():
        print(f"{ICON_ERROR} CPF inválido! Use apenas números.")
        return saldo, extrato
    if len(destino) != 11:
        print(f"{ICON_ERROR} CPF deve conter 11 dígitos.")
        return saldo, extrato
    if not validar_cpf(destino):
        print(f"{ICON_ERROR} CPF inválido!")
        return saldo, extrato
    if destino == usuario:
        print(f"{ICON_ERROR} Não é possível fazer PIX para o próprio CPF.")
        return saldo, extrato
    if destino not in users:
        print(f"{ICON_ERROR} CPF destinatário não encontrado no sistema.")
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
    if now.hour == HORA_LIMITE_PIX and now.minute >= MINUTO_LIMITE_PIX and valor > LIMITE_PIX_NOTURNO:
        print(f"{ICON_ERROR} PIX acima de R$ {LIMITE_PIX_NOTURNO:.2f} não permitido após {HORA_LIMITE_PIX}:{MINUTO_LIMITE_PIX}.")
        return saldo, extrato

    if valor > saldo:
        print(f"{ICON_ERROR} Saldo insuficiente.")
    elif valor <= 0:
        print(f"{ICON_ERROR} Valor inválido.")
    else:
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} - {ICON_PIX} PIX para {destino}: R$ {valor:.2f}\n"
        
        # Adiciona o valor na conta do destinatário
        users[destino]["saldo"] += valor
        users[destino]["extrato"] += f"{timestamp} - {ICON_PIX} PIX recebido de {usuario}: R$ {valor:.2f}\n"
        
        print(f"{ICON_SUCCESS} PIX de R$ {valor:.2f} enviado para {destino} com sucesso!")
    return saldo, extrato


def transferencia(usuario: str, saldo: float, extrato: str) -> Tuple[float, str]:
    """
    Realiza transferência entre contas
    """
    destino = input(f"{ICON_CPF} CPF destinatário (11 dígitos): ")
    if not destino.isdigit():
        print(f"{ICON_ERROR} CPF inválido! Use apenas números.")
        return saldo, extrato
    if len(destino) != 11:
        print(f"{ICON_ERROR} CPF deve conter 11 dígitos.")
        return saldo, extrato
    if not validar_cpf(destino):
        print(f"{ICON_ERROR} CPF inválido!")
        return saldo, extrato
    if destino == usuario:
        print(f"{ICON_ERROR} Não é possível fazer transferência para o próprio CPF.")
        return saldo, extrato
    if destino not in users:
        print(f"{ICON_ERROR} CPF destinatário não encontrado no sistema.")
        return saldo, extrato

    try:
        valor = float(input(f"{ICON_TRANSFER} Informe o valor da transferência: R$ "))
    except ValueError:
        print(f"{ICON_ERROR} Valor inválido.")
        return saldo, extrato

    # Autenticação após informar valor
    if not autenticar(usuario):
        print(f"{ICON_ERROR} Transferência cancelada.")
        return saldo, extrato

    if valor > saldo:
        print(f"{ICON_ERROR} Saldo insuficiente.")
    elif valor <= 0:
        print(f"{ICON_ERROR} Valor inválido.")
    else:
        timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
        saldo -= valor
        extrato += f"{timestamp} - {ICON_TRANSFER} Transferência para {destino}: R$ {valor:.2f}\n"
        
        # Adiciona o valor na conta do destinatário
        users[destino]["saldo"] += valor
        users[destino]["extrato"] += f"{timestamp} - {ICON_TRANSFER} Transferência recebida de {usuario}: R$ {valor:.2f}\n"
        
        print(f"{ICON_SUCCESS} Transferência de R$ {valor:.2f} enviada para {destino} com sucesso!")
    return saldo, extrato


def mostrar_extrato(saldo: float, extrato: str):
    """
    Exibe extrato da conta
    """
    print(f"\n{ICON_MENU}── EXTRATO ──{ICON_MENU}")
    if not extrato:
        print(f"{ICON_INFO} Sem movimentações.")
    else:
        print(extrato, end="")
    print(f"\n💳 Saldo: R$ {saldo:.2f}\n")


def mostrar_historico(usuario: str):
    """
    Exibe histórico detalhado da conta
    """
    user_data = users[usuario]
    print(f"\n{ICON_HISTORY}── HISTÓRICO DA CONTA ──{ICON_HISTORY}")
    print(f"{ICON_USER} Nome: {user_data.get('nome', 'N/A')}")
    print(f"{ICON_CPF} CPF: {usuario}")
    print(f"{ICON_EMAIL} Email: {user_data.get('email', 'N/A')}")
    print(f"{ICON_PHONE} Telefone: {user_data.get('telefone', 'N/A')}")
    print(f"📅 Data de cadastro: {user_data.get('data_cadastro', 'N/A')}")
    print(f"💳 Saldo atual: R$ {user_data['saldo']:.2f}")
    print(f"📊 Total de saques: {user_data['numero_saques']}")
    print(f"📈 Transações hoje: {user_data['numero_transacoes_dia']}/{LIMITE_TRANSACOES_DIARIAS}")
    print(f"📅 Última atualização: {user_data['data_contagem']}\n")


def configurar_conta(usuario: str):
    """
    Permite configurar dados da conta
    """
    user_data = users[usuario]
    print(f"\n{ICON_SETTINGS}── CONFIGURAÇÕES DA CONTA ──{ICON_SETTINGS}")
    
    # Alterar senha
    print(f"\n{ICON_KEY} Alterar senha:")
    senha_atual = input("Senha atual: ")
    if senha_atual == user_data["senha"]:
        while True:
            nova_senha = input("Nova senha (4 dígitos): ")
            if nova_senha.isdigit() and len(nova_senha) == 4:
                user_data["senha"] = nova_senha
                print(f"{ICON_SUCCESS} Senha alterada com sucesso!")
                break
            else:
                print(f"{ICON_ERROR} Senha inválida! Deve ter 4 dígitos.")
    else:
        print(f"{ICON_ERROR} Senha atual incorreta!")
    
    # Alterar email
    print(f"\n{ICON_EMAIL} Alterar email:")
    novo_email = input("Novo email: ")
    if validar_email(novo_email):
        user_data["email"] = novo_email
        print(f"{ICON_SUCCESS} Email alterado com sucesso!")
    else:
        print(f"{ICON_ERROR} Email inválido!")
    
    # Alterar telefone
    print(f"\n{ICON_PHONE} Alterar telefone:")
    novo_telefone = input("Novo telefone: ")
    if validar_telefone(novo_telefone):
        user_data["telefone"] = novo_telefone
        print(f"{ICON_SUCCESS} Telefone alterado com sucesso!")
    else:
        print(f"{ICON_ERROR} Telefone inválido!")


def registrar():
    """
    Registra novo usuário no sistema
    """
    print(f"\n🔐── Cadastro de Usuário ──🔐")
    
    # Validação de CPF
    while True:
        cpf = input(f"{ICON_CPF} CPF (11 dígitos, somente números): ")
        if not cpf.isdigit():
            print(f"{ICON_ERROR} CPF inválido! Use apenas números.")
        elif len(cpf) != 11:
            print(f"{ICON_ERROR} CPF deve conter exatamente 11 dígitos.")
        elif not validar_cpf(cpf):
            print(f"{ICON_ERROR} CPF inválido!")
        elif cpf in users:
            print(f"{ICON_ERROR} CPF já cadastrado!")
        else:
            break

    # Nome do usuário
    nome = input(f"{ICON_USER} Nome completo: ").strip()
    if not nome:
        print(f"{ICON_ERROR} Nome é obrigatório!")
        return

    # Email
    while True:
        email = input(f"{ICON_EMAIL} Email: ").strip()
        if not email:
            print(f"{ICON_ERROR} Email é obrigatório!")
        elif not validar_email(email):
            print(f"{ICON_ERROR} Email inválido!")
        else:
            break

    # Telefone
    while True:
        telefone = input(f"{ICON_PHONE} Telefone: ").strip()
        if not telefone:
            print(f"{ICON_ERROR} Telefone é obrigatório!")
        elif not validar_telefone(telefone):
            print(f"{ICON_ERROR} Telefone inválido!")
        else:
            break

    # Senha
    while True:
        senha = input(f"{ICON_KEY} Crie senha (4 dígitos): ")
        if not (senha.isdigit() and len(senha) == 4):
            print(f"{ICON_ERROR} Senha inválida! Deve ter 4 dígitos.")
        else:
            break

    # Confirmação de senha
    confirma_senha = input(f"{ICON_KEY} Confirme a senha: ")
    if senha != confirma_senha:
        print(f"{ICON_ERROR} Senhas não coincidem!")
        return

    users[cpf] = {
        "senha": senha,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
        "numero_transacoes_dia": 0,
        "data_contagem": date.today(),
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "data_cadastro": datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ativo"
    }
    print(f"{ICON_SUCCESS} Usuário cadastrado com sucesso!")


def login_user():
    """
    Realiza login do usuário
    """
    print(f"\n🔑── Login de Usuário ──🔑")
    cpf = input(f"{ICON_CPF} CPF: ")
    senha = input(f"{ICON_KEY} Senha: ")
    user = users.get(cpf)
    if user and user["senha"] == senha:
        if user.get("status") == "bloqueado":
            print(f"{ICON_ERROR} Conta bloqueada! Entre em contato com o suporte.")
            return None
        print(f"{ICON_SUCCESS} Login bem-sucedido!")
        print(f"Bem-vindo(a), {user.get('nome', 'Usuário')}!\n")
        return cpf
    print(f"{ICON_ERROR} CPF ou senha inválidos!\n")
    return None


def main():
    """
    Função principal do sistema bancário
    """
    # Carrega dados salvos
    carregar_dados()
    
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
            salvar_dados()
            return
        else:
            print(f"{ICON_ERROR} Opção inválida!\n")

    user_data = users[usuario]
    saldo = user_data["saldo"]
    extrato = user_data["extrato"]
    numero_saques = user_data["numero_saques"]
    numero_transacoes_dia = user_data["numero_transacoes_dia"]
    data_contagem = user_data["data_contagem"]
    limite = LIMITE_SAQUE

    while True:
        hoje = date.today()
        if hoje != data_contagem:
            numero_transacoes_dia = 0
            data_contagem = hoje

        opcao = mostrar_menu_transacoes()

        if opcao == "d":
            if numero_transacoes_dia >= LIMITE_TRANSACOES_DIARIAS:
                print(f"🔥 Limite diário de {LIMITE_TRANSACOES_DIARIAS} transações atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato = depositar(usuario, saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "s":
            if numero_transacoes_dia >= LIMITE_TRANSACOES_DIARIAS:
                print(f"🔥 Limite diário de {LIMITE_TRANSACOES_DIARIAS} transações atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato, numero_saques = sacar(usuario, saldo, extrato, numero_saques, limite)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "p":
            if numero_transacoes_dia >= LIMITE_TRANSACOES_DIARIAS:
                print(f"🔥 Limite diário de {LIMITE_TRANSACOES_DIARIAS} transações atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato = pix(usuario, saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "t":
            if numero_transacoes_dia >= LIMITE_TRANSACOES_DIARIAS:
                print(f"🔥 Limite diário de {LIMITE_TRANSACOES_DIARIAS} transações atingido!")
            else:
                extrato_pre = extrato
                saldo, extrato = transferencia(usuario, saldo, extrato)
                if extrato != extrato_pre:
                    numero_transacoes_dia += 1

        elif opcao == "e":
            mostrar_extrato(saldo, extrato)

        elif opcao == "v":
            print(f"👀 Saldo: R$ {saldo:.2f}\n")

        elif opcao == "h":
            mostrar_historico(usuario)

        elif opcao == "c":
            configurar_conta(usuario)

        elif opcao == "q":
            print(f"🙏 Obrigado! Até logo!")
            user_data.update({
                "saldo": saldo,
                "extrato": extrato,
                "numero_saques": numero_saques,
                "numero_transacoes_dia": numero_transacoes_dia,
                "data_contagem": data_contagem
            })
            salvar_dados()
            break

        else:
            print(f"{ICON_ERROR} Operação inválida!")

        # Atualiza dados do usuário
        user_data.update({
            "saldo": saldo,
            "extrato": extrato,
            "numero_saques": numero_saques,
            "numero_transacoes_dia": numero_transacoes_dia,
            "data_contagem": data_contagem
        })


if __name__ == "__main__":
    main()
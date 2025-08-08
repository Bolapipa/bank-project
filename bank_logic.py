from datetime import datetime, date
import pytz
import json
import os
import re
import random
from typing import Dict, Any, Optional, Tuple

# --- Constantes do Sistema ---
LIMITE_SAQUE = 500.0
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACOES_DIARIAS = 10
LIMITE_PIX_NOTURNO = 500.0
HORA_LIMITE_PIX = 23
MINUTO_LIMITE_PIX = 59
DATA_FILE = "bank_data.json"
TZ = pytz.timezone("America/Sao_Paulo")

# --- Mercado Simulado ---
# Preços base e volatilidade para simulação
SIMULATED_MARKET = {
    "cripto": {
        "BTC": {"price": 350000.0, "volatility": 0.05},
        "ETH": {"price": 15000.0, "volatility": 0.08},
    },
    "acoes": {
        "EPIC-A": {"price": 150.0, "volatility": 0.02},
        "GEM-B": {"price": 85.0, "volatility": 0.03},
    }
}

# Armazenamento de usuários em memória
users = {}

# --- Funções de Validação ---
def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    return cpf[-2:] == f"{digito1}{digito2}"

def validar_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_telefone(telefone: str) -> bool:
    telefone = re.sub(r'[^0-9]', '', telefone)
    return len(telefone) in [10, 11]

# --- Persistência de Dados ---
def salvar_dados():
    try:
        dados_para_salvar = {}
        for cpf, user_data in users.items():
            dados_para_salvar[cpf] = user_data.copy()
            if isinstance(user_data.get("data_contagem"), date):
                dados_para_salvar[cpf]["data_contagem"] = user_data["data_contagem"].isoformat()
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=2, ensure_ascii=False)
        return True, "Dados salvos com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar dados: {e}"

def carregar_dados():
    global users
    if not os.path.exists(DATA_FILE):
        return False, "Arquivo de dados não encontrado."
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            dados_carregados = json.load(f)
        for cpf, user_data in dados_carregados.items():
            if isinstance(user_data.get("data_contagem"), str):
                user_data["data_contagem"] = date.fromisoformat(user_data["data_contagem"])
            # Garante que usuários antigos tenham a estrutura de portfólio
            if "portfolio" not in user_data:
                user_data["portfolio"] = {"cripto": {}, "acoes": {}}
        users = dados_carregados
        return True, "Dados carregados com sucesso!"
    except Exception as e:
        users = {}
        return False, f"Erro ao carregar dados: {e}"

# --- Lógica de Mercado ---
def get_market_prices() -> Dict[str, Any]:
    """Simula a flutuação dos preços do mercado."""
    market_now = {}
    for category, assets in SIMULATED_MARKET.items():
        market_now[category] = {}
        for asset, data in assets.items():
            price = data["price"]
            volatility = data["volatility"]
            change = random.uniform(-volatility, volatility)
            new_price = price * (1 + change)
            market_now[category][asset] = round(new_price, 2)
    return market_now

# --- Gestão de Usuários ---
def registrar_usuario(cpf: str, nome: str, email: str, telefone: str, senha: str, confirma_senha: str) -> Tuple[bool, str]:
    if not validar_cpf(cpf): return False, "CPF inválido!"
    if cpf in users: return False, "CPF já cadastrado!"
    if not nome.strip(): return False, "Nome é obrigatório!"
    if not validar_email(email): return False, "Email inválido!"
    if not validar_telefone(telefone): return False, "Telefone inválido!"
    if not (senha.isdigit() and len(senha) == 4): return False, "Senha inválida! Deve ter 4 dígitos."
    if senha != confirma_senha: return False, "Senhas não coincidem!"

    users[cpf] = {
        "senha": senha, "saldo": 0.0, "extrato": "",
        "numero_saques": 0, "numero_transacoes_dia": 0,
        "data_contagem": date.today(), "nome": nome, "email": email, "telefone": telefone,
        "data_cadastro": datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ativo",
        "portfolio": {
            "cripto": {},
            "acoes": {}
        }
    }
    salvar_dados()
    return True, "Usuário cadastrado com sucesso!"

def login_user(cpf: str, senha: str) -> Tuple[bool, str, Optional[str]]:
    user = users.get(cpf)
    if user and user["senha"] == senha:
        if user.get("status") == "bloqueado":
            return False, "Conta bloqueada!", None
        hoje = date.today()
        if user.get("data_contagem") != hoje:
            user["numero_transacoes_dia"] = 0
            user["numero_saques"] = 0
            user["data_contagem"] = hoje
            salvar_dados()
        return True, f"Login bem-sucedido!", cpf
    return False, "CPF ou senha inválidos!", None

def get_user_data(cpf: str) -> Optional[Dict[str, Any]]:
    return users.get(cpf)

# --- Operações Financeiras ---
def depositar(usuario_cpf: str, valor: float) -> Tuple[bool, str]:
    if valor <= 0: return False, "Valor de depósito inválido."
    user_data = users[usuario_cpf]
    if user_data["numero_transacoes_dia"] >= LIMITE_TRANSACOES_DIARIAS:
        return False, f"Limite diário de transações atingido!"
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    user_data["saldo"] += valor
    user_data["extrato"] += f"{timestamp} - Depósito: +R$ {valor:.2f}\n"
    user_data["numero_transacoes_dia"] += 1
    salvar_dados()
    return True, f"Depósito de R$ {valor:.2f} realizado!"

def sacar(usuario_cpf: str, valor: float) -> Tuple[bool, str]:
    user_data = users[usuario_cpf]
    if user_data["numero_transacoes_dia"] >= LIMITE_TRANSACOES_DIARIAS: return False, f"Limite diário de transações atingido!"
    if user_data["numero_saques"] >= LIMITE_SAQUES_DIARIOS: return False, f"Limite de saques diários atingido!"
    if valor <= 0: return False, "Valor de saque inválido."
    if valor > user_data["saldo"]: return False, "Saldo insuficiente."
    if valor > LIMITE_SAQUE: return False, f"Limite por saque: R$ {LIMITE_SAQUE:.2f}."
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    user_data["saldo"] -= valor
    user_data["extrato"] += f"{timestamp} - Saque: -R$ {valor:.2f}\n"
    user_data["numero_saques"] += 1
    user_data["numero_transacoes_dia"] += 1
    salvar_dados()
    return True, f"Saque de R$ {valor:.2f} realizado!"

def pix(usuario_cpf: str, destino_cpf: str, valor: float) -> Tuple[bool, str]:
    user_data = users[usuario_cpf]
    if not validar_cpf(destino_cpf): return False, "CPF do destinatário inválido!"
    if destino_cpf not in users: return False, "CPF do destinatário não encontrado."
    if usuario_cpf == destino_cpf: return False, "Não é possível enviar PIX para si mesmo."
    if valor > user_data["saldo"]: return False, "Saldo insuficiente."
    # ... (outras validações de limite e horário)
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    user_data["saldo"] -= valor
    user_data["extrato"] += f"{timestamp} - PIX Enviado para {destino_cpf}: -R$ {valor:.2f}\n"
    users[destino_cpf]["saldo"] += valor
    users[destino_cpf]["extrato"] += f"{timestamp} - PIX Recebido de {usuario_cpf}: +R$ {valor:.2f}\n"
    salvar_dados()
    return True, f"PIX de R$ {valor:.2f} enviado!"

def get_extrato(usuario_cpf: str) -> Tuple[str, float]:
    user_data = users[usuario_cpf]
    saldo = user_data.get("saldo", 0.0)
    extrato = user_data.get("extrato", "Sem movimentações.")
    return extrato if extrato.strip() else "Sem movimentações.", saldo

# --- Operações de Investimento ---
def comprar_investimento(usuario_cpf: str, categoria: str, ativo: str, quantidade: float) -> Tuple[bool, str]:
    user_data = users[usuario_cpf]
    precos_atuais = get_market_prices()
    preco_unitario = precos_atuais[categoria][ativo]
    custo_total = preco_unitario * quantidade

    if user_data["saldo"] < custo_total:
        return False, "Saldo insuficiente para a compra."

    # Deduz do saldo e adiciona ao extrato
    user_data["saldo"] -= custo_total
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    user_data["extrato"] += f"{timestamp} - Compra {ativo}: {quantidade} un. a R$ {preco_unitario:.2f} (-R$ {custo_total:.2f})\n"

    # Adiciona ao portfólio
    portfolio_cat = user_data["portfolio"][categoria]
    portfolio_cat[ativo] = portfolio_cat.get(ativo, 0) + quantidade
    
    salvar_dados()
    return True, f"Compra de {quantidade} {ativo} realizada com sucesso!"

def vender_investimento(usuario_cpf: str, categoria: str, ativo: str, quantidade: float) -> Tuple[bool, str]:
    user_data = users[usuario_cpf]
    portfolio_cat = user_data["portfolio"][categoria]

    if ativo not in portfolio_cat or portfolio_cat[ativo] < quantidade:
        return False, "Quantidade de ativo insuficiente para a venda."

    precos_atuais = get_market_prices()
    preco_unitario = precos_atuais[categoria][ativo]
    valor_total = preco_unitario * quantidade

    # Deduz do portfólio
    portfolio_cat[ativo] -= quantidade
    if portfolio_cat[ativo] == 0:
        del portfolio_cat[ativo]

    # Adiciona ao saldo e ao extrato
    user_data["saldo"] += valor_total
    timestamp = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    user_data["extrato"] += f"{timestamp} - Venda {ativo}: {quantidade} un. a R$ {preco_unitario:.2f} (+R$ {valor_total:.2f})\n"
    
    salvar_dados()
    return True, f"Venda de {quantidade} {ativo} realizada com sucesso!"

# Carregar os dados ao iniciar o módulo
carregar_dados()
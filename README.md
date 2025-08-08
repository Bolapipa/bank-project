# Sistema Bancário Python - Versão Melhorada

## 🚀 Melhorias Implementadas

### 1. **Validação de CPF**
- Implementação do algoritmo oficial brasileiro de validação de CPF
- Verificação de dígitos verificadores
- Prevenção de CPFs com todos os dígitos iguais

### 2. **Persistência de Dados**
- Salvamento automático em arquivo JSON (`bank_data.json`)
- Carregamento automático dos dados ao iniciar o sistema
- Preservação de todas as informações entre sessões

### 3. **Novas Funcionalidades**

#### 📧 **Cadastro Completo**
- Nome completo do usuário
- Validação de email
- Validação de telefone brasileiro
- Confirmação de senha

#### 🔄 **Transferência entre Contas**
- Nova opção de transferência além do PIX
- Validação de CPF destinatário
- Atualização automática do saldo do destinatário

#### 📊 **Histórico Detalhado**
- Informações completas da conta
- Estatísticas de uso
- Data de cadastro e última atualização

#### ⚙️ **Configurações da Conta**
- Alteração de senha
- Atualização de email
- Modificação de telefone

### 4. **Melhorias de Segurança**

#### 🔐 **Autenticação Aprimorada**
- Limite de tentativas de senha (3 tentativas)
- Feedback sobre tentativas restantes
- Verificação de status da conta (ativo/bloqueado)

#### 🛡️ **Validações Robustas**
- Validação de email com regex
- Validação de telefone brasileiro
- Verificação de CPF existente no sistema

### 5. **Organização e Código**

#### 📝 **Type Hints**
- Adição de type hints em todas as funções
- Melhor documentação do código
- Facilita manutenção e debugging

#### 🏗️ **Constantes Configuráveis**
```python
LIMITE_SAQUE = 500.0
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACOES_DIARIAS = 10
LIMITE_PIX_NOTURNO = 500.0
```

#### 📚 **Documentação**
- Docstrings em todas as funções
- Comentários explicativos
- Estrutura modular

### 6. **Interface Melhorada**

#### 🎨 **Novos Ícones**
- Ícones para todas as funcionalidades
- Interface mais intuitiva
- Feedback visual aprimorado

#### 📋 **Menu Expandido**
```
✨─── Operações Bancárias ───✨
💰 [d] Depositar
💸 [s] Saque
⚡ [p] Pix
🔄 [t] Transferência
📄 [e] Extrato
👀 [v] Saldo
📊 [h] Histórico
⚙️ [c] Configurações
❌ [q] Sair
```

### 7. **Funcionalidades Avançadas**

#### 💾 **Persistência Inteligente**
- Salvamento automático ao sair
- Carregamento automático ao iniciar
- Tratamento de erros de I/O

#### 🔄 **Transferências Reais**
- PIX e Transferência atualizam saldo do destinatário
- Registro em ambas as contas
- Validação de existência do destinatário

#### 📈 **Controle de Limites**
- Limite de 3 saques diários
- Limite de 10 transações diárias
- Limite de PIX noturno (após 23:59)

## 🛠️ Como Usar

### Instalação
```bash
# Instalar dependências
pip install pytz

# Executar o sistema
python bank_code.py
```

### Primeiro Uso
1. Escolha `[c]` para cadastro
2. Preencha todos os dados solicitados
3. Faça login com `[l]`
4. Explore as funcionalidades disponíveis

### Funcionalidades Principais

#### 💰 **Depósito**
- Valor positivo obrigatório
- Autenticação por senha
- Registro no extrato

#### 💸 **Saque**
- Limite de R$ 500 por saque
- Máximo 3 saques diários
- Verificação de saldo

#### ⚡ **PIX**
- Validação de CPF destinatário
- Limite noturno (R$ 500 após 23:59)
- Transferência automática entre contas

#### 🔄 **Transferência**
- Nova funcionalidade
- Mesmas validações do PIX
- Sem limite noturno

#### 📄 **Extrato**
- Histórico completo de transações
- Saldo atualizado
- Formatação clara

#### 📊 **Histórico**
- Informações pessoais
- Estatísticas de uso
- Data de cadastro

#### ⚙️ **Configurações**
- Alteração de senha
- Atualização de dados pessoais
- Validação de novos dados

## 🔧 Configurações

### Limites Configuráveis
```python
LIMITE_SAQUE = 500.0              # Limite por saque
LIMITE_SAQUES_DIARIOS = 3         # Máximo saques por dia
LIMITE_TRANSACOES_DIARIAS = 10    # Máximo transações por dia
LIMITE_PIX_NOTURNO = 500.0        # Limite PIX após 23:59
```

### Arquivo de Dados
- `bank_data.json`: Armazena todos os dados dos usuários
- Formato JSON legível
- Backup automático

## 🚨 Segurança

### Validações Implementadas
- ✅ CPF válido (algoritmo oficial)
- ✅ Email válido (regex)
- ✅ Telefone brasileiro
- ✅ Senha forte (4 dígitos)
- ✅ Limite de tentativas
- ✅ Verificação de saldo
- ✅ Controle de limites diários

### Proteções
- 🔒 Autenticação obrigatória
- 🛡️ Validação de dados de entrada
- 📊 Controle de transações
- ⏰ Limites temporais

## 📈 Melhorias Futuras Sugeridas

1. **Criptografia de Senhas**
   - Hash bcrypt para senhas
   - Salt único por usuário

2. **Logs de Auditoria**
   - Registro de todas as operações
   - Logs de segurança

3. **Interface Web**
   - API REST
   - Interface gráfica

4. **Banco de Dados**
   - SQLite/PostgreSQL
   - Migrations

5. **Notificações**
   - Email de confirmação
   - SMS de transações

6. **Relatórios**
   - Extrato em PDF
   - Relatórios mensais

## 🤝 Contribuição

Para contribuir com melhorias:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste todas as funcionalidades
5. Submeta um pull request

## 📄 Licença

Este projeto é de uso educacional e demonstração de conceitos de programação Python.

---

**Desenvolvido com ❤️ para aprendizado de Python e boas práticas de desenvolvimento.**
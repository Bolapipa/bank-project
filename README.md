Bank Project
<img src="https://img.icons8.com/color/96/000000/bank.png" align="right" width="120"/>
📝 O que este projeto faz?
Bem-vindo ao Bank Project!
Este projeto é um sistema bancário didático em Python, criado para simular as principais operações de uma conta corrente via terminal, com foco em conceitos de lógica, funções, manipulação de dados e boas práticas de código.

🔄 Atualizações e Novas Funcionalidades
Nas últimas versões do código, incorporamos:

Cadastro e Login de Usuário

Registro por CPF (11 dígitos, sem traços) e senha numérica (mínimo 4 dígitos).

Validação de CPF único: não permite duplicar contas no sistema.

Tela de login obrigatória antes de acessar as demais operações.

Menu Case-Insensitive

Agora o terminal aceita comandos em letras maiúsculas e minúsculas, sem distinção.

Segurança com Senha em Operações Sensíveis

A cada depósito, saque ou PIX, o sistema solicita confirmação de senha.

Funcionalidade PIX (⚡)

Transferências entre contas cadastradas.

Não permite enviar PIX para o próprio CPF.

Limite de valor: até R$ 500,00 (com restrição de horário após as 23:59 – fuso “America/Sao_Paulo” via pytz).

Limite Diário de Transações

Máximo de 10 transações (depósitos, saques e PIX) por dia.

Ao atingir o limite, novas operações são bloqueadas até a virada do dia.

Extrato Detalhado com Data e Hora

Cada movimentação exibe data e hora no formato DD/MM/YYYY HH:MM:SS.

Fuso horário configurado para São Paulo (America/Sao_Paulo).

Melhoria Visual no Terminal

Ícones amigáveis para cada opção:

💰 [d] Depositar

💸 [s] Sacar

⚡ [p] PIX

👀 [v] Saldo

📄 [e] Extrato

🔑 [l] Login/Cadastro

❌ [q] Sair

Mensagens de sucesso e erro com ícones (✅, ❌) e textos mais descritivos.

Funcionalidades
✅ Cadastro e Login de usuários por CPF e senha

💰 Depósitos com validação de valor e confirmação de senha

💸 Saques respeitando saldo e limite, com confirmação de senha

⚡ PIX entre contas, sem enviar para si mesmo, limite de R$ 500,00 após 23:59, confirmação de senha

👀 Consulta de Saldo a qualquer momento

📄 Extrato com histórico completo e timestamps

🔒 Segurança reforçada: senha em operações sensíveis

🚫 Limite Diário de 10 transações por conta

Tecnologias utilizadas
Python 3.x

Biblioteca pytz (fuso horário “America/Sao_Paulo”)

Como executar o projeto
Clone este repositório.

Instale dependências (separadas):

bash
Copiar
Editar
pip install pytz
Execute:

bash
Copiar
Editar
python bank.py
No menu inicial, cadastre um novo usuário ou faça login com CPF e senha.

Utilize as opções para operar sua conta.

Objetivos de aprendizado
Praticar estruturas de decisão e repetição em Python

Criar e modularizar funções

Tratar validação de entradas e erros

Implementar autenticação básica e segurança

Simular operações bancárias reais e restrições (PIX, limite de transações)

<img src="https://img.icons8.com/color/96/000000/money.png" width="80"/> *Feito para estudos e aprendizado!*
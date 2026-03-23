# 💇‍♀️ Sistema de Agendamento para Salão de Beleza

Sistema completo de agendamento desenvolvido com **FastAPI (backend)** e **JavaScript puro (frontend)**, com foco em organização de horários, controle de serviços e experiência do usuário.

---

## 📌 Sobre o Projeto

Este sistema foi desenvolvido com o objetivo de simular um ambiente real de um salão de beleza, permitindo:

- Seleção de serviços
- Agendamento com data e horário
- Verificação de disponibilidade
- Controle de status
- Visualização gerencial

O sistema também inclui regras de negócio importantes como **conflito de horários, horário de funcionamento e cálculo automático de duração e valor total**.

---

## 🚀 Tecnologias Utilizadas

### 🔹 Backend
- Python
- FastAPI
- SQLite

### 🔹 Frontend
- HTML
- CSS
- JavaScript (Vanilla JS)

---

## ⚙️ Funcionalidades

### 💅 Serviços
- Listagem de serviços via API  
- Exibição em cards interativos  
- Seleção e remoção de serviços  
- Cálculo automático de:
  - Total (R$)
  - Duração (minutos)
  - Quantidade  

---

### 📅 Agendamento

- Criação de agendamento (`POST /agendamentos`)
- Campos:
  - Nome do cliente
  - Serviços (lista de IDs)
  - Data
  - Horário
  - Observação (opcional)

---

### 🔒 Validações implementadas

- Campos obrigatórios
- Cliente criado automaticamente se não existir  
- Verificação de conflito de horários  
- Verificação de horário de funcionamento (08:00 às 18:00)  
- Verificação de disponibilidade antes do envio  
- Bloqueio de edição com menos de 2 dias de antecedência  

---

### ⏱️ Controle de Horários

- Cálculo automático de duração baseado nos serviços  
- Conversão de horários para minutos  
- Verificação de sobreposição de agendamentos  

---

### 🔄 Status de Agendamento

Status disponíveis:

- pendente  
- confirmado  
- cancelado  
- concluído  

Também é possível controlar o status de cada serviço individualmente.

---

### 📊 Módulo Gerencial

Endpoint:

GET /gerencial/desempenho-semanal


Retorna:

- Total de agendamentos
- Faturamento da semana
- Total de cancelamentos
- Serviços mais solicitados  

---

### 📜 Histórico

Consulta por período:


GET /agendamentos/historico


Permite visualizar todos os agendamentos detalhados entre duas datas.

---

### 🧑‍💻 Área Admin

- Listagem de agendamentos
- Edição de agendamento
- Confirmação rápida
- Visualização de histórico
- Resumo gerencial

---

## 🗄️ Banco de Dados

O sistema utiliza **SQLite** com as seguintes tabelas:

- clientes  
- servicos  
- agendamentos  
- agendamento_servicos  

Criadas automaticamente ao iniciar o sistema.

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

git clone <seu-repositorio>
cd projeto
2. Criar ambiente virtual
python -m venv venv

Ativar:

Windows:
venv\Scripts\activate
Linux/Mac:
source venv/bin/activate
3. Instalar dependências
pip install fastapi uvicorn jinja2
4. Rodar o servidor
uvicorn app.main:app --reload
5. Acessar no navegador
Sistema:
http://localhost:8000
Área admin:
http://localhost:8000/admin
Documentação da API:
http://localhost:8000/docs
💡 Diferenciais do Projeto
Validação completa de regras de negócio
Controle de conflitos de horário
Sistema de status (agendamento e serviços)
Sugestão inteligente de agendamento
Dashboard gerencial com métricas reais
Interface moderna e responsiva
Código organizado por camadas
📈 Melhorias Futuras
Autenticação de usuários (login)
Integração com WhatsApp
Notificações automáticas
Agenda visual (calendário)
Multi-profissionais
Deploy em nuvem
👩‍💻 Autora

Maria Julia Felix

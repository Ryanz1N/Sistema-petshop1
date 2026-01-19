# Sistema de Gestão para PetShop (ERP & Agendamento)

Sistema completo desenvolvido em **Django** e **Bootstrap 5** para gerenciamento de clínicas veterinárias e pet shops.  
O sistema permite o controle de agendamentos de serviços (banho e tosa), vendas de produtos (PDV), gestão de estoque e administração de usuários.

---

## 🎯 Objetivo do Sistema

Desenvolver um sistema web para aplicar os conceitos estudados na disciplina **Programação Web II**, contemplando:
- Autenticação de usuários
- Modelagem de banco de dados relacional
- Organização em camadas (MVC/MVT)
- Persistência de dados

---

## 🚀 Funcionalidades Principais

- **Controle de Acesso**
  - Login via e-mail
  - Cadastro de funcionários
  - Perfis de acesso

- **Agenda Inteligente (Kanban)**
  - Visualização por colunas (Marcado, Em Serviço, Pronto)
  - Navegação por datas
  - Alerta visual de serviços atrasados

- **Ponto de Venda (PDV)**
  - Venda rápida de produtos
  - Baixa automática de estoque

- **Gestão de Serviços**
  - Cadastro de clientes e pets
  - Consumo interno de produtos durante o atendimento
  - Checklist de finalização e observações

- **Histórico**
  - Histórico completo de vendas e atendimentos

---

## 🗄️ Banco de Dados (Diagrama ER)

Abaixo está a estrutura do banco de dados relacional do sistema:

```mermaid
erDiagram
    Funcionario ||--|| Profile : "possui"
    Funcionario ||--o{ Agendamento : "registra"
    Funcionario ||--o{ Venda : "realiza"

    Cliente ||--o{ Pet : "possui"
    Cliente ||--o{ Venda : "realiza"

    Pet ||--o{ Agendamento : "recebe"

    Servico ||--o{ Agendamento : "define"

    Agendamento ||--o{ ConsumoServico : "gera"

    Produto ||--o{ ConsumoServico : "utilizado em"
    Produto ||--o{ ItemVenda : "vendido em"

    Venda ||--o{ ItemVenda : "contém"

    Funcionario {
        int id PK
        string username
        string password
    }

    Profile {
        int id PK
        int funcionario_id FK
        boolean is_funcionario
    }

    Cliente {
        int id PK
        string nome
        string telefone
        string email
        string endereco
        datetime data_cadastro
    }

    Pet {
        int id PK
        int cliente_id FK
        string nome
        string especie
        string raca
        string observacoes
    }

    Servico {
        int id PK
        string nome
        int duracao_estimada
        decimal preco
    }

    Produto {
        int id PK
        string nome
        int quantidade
        decimal preco_venda
    }

    Agendamento {
        int id PK
        int pet_id FK
        int servico_id FK
        int funcionario_id FK
        datetime data_inicio
        datetime data_fim
        string status
        text observacoes
    }

    ConsumoServico {
        int id PK
        int agendamento_id FK
        int produto_id FK
        int quantidade
    }

    Venda {
        int id PK
        int cliente_id FK
        int funcionario_id FK
        datetime data
        decimal valor_total
    }

    ItemVenda {
        int id PK
        int venda_id FK
        int produto_id FK
        int quantidade
        decimal subtotal
    }
```

Como Rodar o Projeto

Siga os passos abaixo para executar o sistema localmente.

1. Clonar o repositório
git clone https://github.com/Ryanz1N/Sistema-petshop1.git
cd Sistema-petshop1

2. Criar e ativar o ambiente virtual

Windows

python -m venv venv
venv\Scripts\activate


Linux / Mac

python3 -m venv venv
source venv/bin/activate

3. Instalar dependências

Instale o Django manualmente (caso não exista requirements.txt):

pip install django

4. Configurar o Banco de Dados

O projeto utiliza SQLite, já incluso no arquivo db.sqlite3.
Caso necessário, execute as migrações:

python manage.py migrate

5. Criar um Superusuário (Admin)

Para acessar o painel administrativo do Django:

python manage.py createsuperuser

6. Iniciar o Servidor
python manage.py runserver


Acesse no navegador:
👉 http://127.0.0.1:8000/

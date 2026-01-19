#  Sistema de Gestão para PetShop (ERP & Agendamento)

Sistema completo desenvolvido em **Django** e **Bootstrap 5** para gerenciamento de clínicas veterinárias e pet shops. O sistema controla desde o agendamento de serviços (banho e tosa) até vendas de produtos (PDV) e gestão de estoque.

---

##  Funcionalidades Principais

- ** Controle de Acesso:** Login via E-mail, cadastro de funcionários e perfis de acesso.
- ** Agenda Inteligente (Kanban):**
  - Visualização por colunas (Marcado, Em Serviço, Pronto).
  - Navegação por datas.
  - Alerta visual de serviços atrasados.
- ** Ponto de Venda (PDV):**
  - Venda de produtos rápida.
  - Baixa automática de estoque.
- ** Gestão de Serviços:**
  - Cadastro de Clientes e Pets.
  - Consumo interno (produtos gastos durante o banho/tosa).
  - Checklist de finalização e observações.
- ** Histórico: **
  - Histórico completo de vendas e atendimentos.
---

## Banco de Dados (Diagrama ER)

Abaixo está a estrutura do banco de dados relacional do sistema:

```mermaid
erDiagram
    Funcionario ||--|| Profile : "possui (1:1)"
    Funcionario ||--o{ Agendamento : "atende/registra (1:N)"
    Funcionario ||--o{ Venda : "registra (1:N)"

    Cliente ||--o{ Pet : "dono de (1:N)"
    Cliente ||--o{ Venda : "realiza (1:N)"

    Pet ||--o{ Agendamento : "recebe (1:N)"

    Servico ||--o{ Agendamento : "define (1:N)"

    Agendamento ||--o{ ConsumoServico : "gera (1:N)"
    
    Produto ||--o{ ConsumoServico : "usado em (1:N)"
    Produto ||--o{ ItemVenda : "vendido em (1:N)"

    Venda ||--o{ ItemVenda : "contém (1:N)"

    Funcionario {
        int id PK
        string username
        string password
    }

    Profile {
        int id PK
        int user_id FK
        bool is_funcionario
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
        int dono_id FK
        string nome
        string especie
        string raca
        string alertas
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
git clone <link-do-repositorio>
cd sistema-petshop

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

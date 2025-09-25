# Telephony Dashboard

## Descrição

Este projeto é uma aplicação web completa que consome uma API de chamadas telefônicas, armazena os dados, gerencia usuários e exibe métricas em um dashboard interativo. A aplicação é composta por um backend em Python com FastAPI, um frontend em React e um banco de dados PostgreSQL, todos orquestrados com Docker.

## Funcionalidades

### Backend

- **Autenticação JWT:** Sistema de autenticação seguro para proteger as rotas.
- **CRUD de Usuários:** Gerenciamento de usuários (criação, leitura, atualização, exclusão).
- **Ingestão de Dados:** Consumo e armazenamento de dados de chamadas de uma API externa.
- **API de Métricas:** Endpoints para servir os KPIs e dados para os gráficos do dashboard.
- **Documentação Automática:** Documentação interativa da API com Swagger UI.

### Frontend

- **Login de Usuário:** Página de login para autenticação.
- **Dashboard Interativo:**
  - **KPIs:** Exibição dos principais indicadores (Total de Chamadas, Chamadas Atendidas, ASR, ACD).
  - **Gráfico de Série Temporal:** Volume de chamadas por hora ou por dia.
  - **Tabela de Chamadas:** Visualização detalhada das chamadas com paginação.

## Tecnologias Utilizadas

- **Backend:**
  - Python 3.11
  - FastAPI
  - SQLAlchemy
  - Alembic
  - PostgreSQL
  - Pydantic
  - Uvicorn
- **Frontend:**
  - React
  - Vite
  - Zustand
  - Axios
  - Recharts
  - Tailwind CSS
- **DevOps:**
  - Docker
  - Docker Compose

## Estrutura do Projeto

```
telephony-dashboard/
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Pré-requisitos

- Docker
- Docker Compose

## Como Executar o Projeto

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/gab-i-alves/telephony-dashboard
    cd telephony-dashboard
    ```

2.  **Configure as variáveis de ambiente:**

    - Crie uma cópia do arquivo `.env.example` e renomeie para `.env`.
    - Preencha as variáveis de ambiente no arquivo `.env` com as suas configurações.

3.  **Suba os contêineres com Docker Compose:**

    ```bash
    docker compose up -d --build
    ```

    _(Aguarde um momento até o contêiner do banco de dados (`db`) estar totalmente online antes de prosseguir)._

4.  **Acesse as aplicações:**

    - **Frontend:** [http://localhost:3000/login](http://localhost:3000/login)
    - **Backend (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

5.  **Execute as migrações do banco de dados:**

    ```bash
    docker compose exec api alembic upgrade head
    ```

## Endpoints da API

A documentação completa dos endpoints da API está disponível na interface do Swagger UI, que pode ser acessada em [http://localhost:8000/docs](http://localhost:8000/docs).

## Executando os Testes

Para executar os testes do backend, utilize o seguinte comando:

```bash
docker compose exec api pytest app/tests/
```

## Variáveis de Ambiente

As seguintes variáveis de ambiente precisam ser configuradas no arquivo `.env`:

- `POSTGRES_USER`: Usuário do banco de dados PostgreSQL.
- `POSTGRES_PASSWORD`: Senha do banco de dados PostgreSQL.
- `POSTGRES_DB`: Nome do banco de dados PostgreSQL.
- `DATABASE_URL`: URL de conexão com o banco de dados.
- `SECRET_KEY`: Chave secreta para a geração de tokens JWT.
- `ALGORITHM`: Algoritmo para a geração de tokens JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tempo de expiração do token de acesso em minutos.

## Como Popular os Dados (Passo a Passo Manual)

Para visualizar os dados no dashboard, é necessário primeiro criar um usuário e executar a ingestão das chamadas através da API. Siga os passos abaixo:

#### **Passo 1: Acesse a Documentação da API**

Abra o seu navegador e acesse a documentação interativa do Swagger: [**http://localhost:8000/docs**](http://localhost:8000/docs)

#### **Passo 2: Crie um Usuário Administrador**

1.  Na lista de endpoints, encontre **`POST /users/`** e clique para expandir.
2.  Clique no botão **"Try it out"**.
3.  No corpo da requisição (`Request body`), insira os dados do usuário que deseja criar. Por exemplo:
    ```json
    {
      "email": "admin@example.com",
      "password": "admin"
    }
    ```
4.  Clique no botão **"Execute"**. Você deve receber uma resposta com código `201`, confirmando que o usuário foi criado.

#### **Passo 3: Faça Login para Obter o Token de Acesso**

1.  Encontre o endpoint **`POST /login`** e expanda-o.
2.  Clique em **"Try it out"**.
3.  Preencha os campos do formulário com as credenciais do usuário que você acabou de criar:
    - `username`: **`admin@example.com`**
    - `password`: **`admin`**
4.  Clique em **"Execute"**.
5.  Na resposta (`Response body`), você receberá um `access_token`. **Copie este token inteiro**, pois você o usará no próximo passo.

#### **Passo 4: Autorize as Requisições no Swagger**

1.  No topo direito da página do Swagger, clique no botão **"Authorize"**.
2.  Na janela que aparecer, no campo **client_secret**, cole o token que você copiou. Deve ficar assim:
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
3.  Clique em **"Authorize"** e depois em **"Close"**. Agora você está autenticado para usar os endpoints protegidos.

#### **Passo 5: Execute a Ingestão de Dados**

1.  Encontre o endpoint **`POST /calls/ingest`** e expanda-o.
2.  Clique em **"Try it out"**.
3.  Clique em **"Execute"**. Este processo irá buscar os dados da API externa e salvá-los no seu banco de dados.

#### **Passo 6: Visualize o Dashboard**

1.  Agora, acesse a interface do frontend: [**http://localhost:3000/login**](http://localhost:3000/login)
2.  Faça login com o usuário criado (**`admin@example.com`** / **`admin`**).
3.  Pronto\! O dashboard agora exibirá os KPIs, o gráfico e a tabela com os dados das chamadas que foram ingeridas.

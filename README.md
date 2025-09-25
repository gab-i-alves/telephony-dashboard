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
    docker-compose up -d --build
    ```

4.  **Acesse as aplicações:**

    - **Frontend:** [http://localhost:3000](http://localhost:3000)
    - **Backend (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

5.  **Execute as migrações do banco de dados:**

    ```bash
    docker-compose exec api alembic upgrade head
    ```

## Endpoints da API

A documentação completa dos endpoints da API está disponível na interface do Swagger UI, que pode ser acessada em [http://localhost:8000/docs](http://localhost:8000/docs).

## Executando os Testes

Para executar os testes do backend, utilize o seguinte comando:

```bash
docker-compose exec api pytest app/tests/
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

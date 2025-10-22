# Meu Pedaço Favorito

Plataforma SaaS para pizzarias venderem pizzas por pedaço. Este é o monorepo contendo o frontend (Next.js) e o backend (FastAPI).

## Visão do Produto & Stack

O objetivo é criar um MVP de uma plataforma multi-tenant onde cada pizzaria (tenant) pode gerenciar seu próprio cardápio, receber pedidos e configurar sua loja online.

- **Backend:** FastAPI (Python)
- **Frontend:** Next.js 15 (React/TypeScript)
- **Banco de Dados:** PostgreSQL
- **Cache/Sessões:** Redis
- **Containerização:** Docker

## Setup Rápido

Para rodar o ambiente de desenvolvimento completo, certifique-se de ter o Docker e o Docker Compose instalados.

```bash
# 1. Clone o repositório (se aplicável)

# 2. Copie os arquivos de ambiente
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Suba os containers
docker-compose up --build
```

Após a execução, os serviços estarão disponíveis nos seguintes endereços:

- **Frontend (Site Principal):** [http://localhost:3000](http://localhost:3000)
- **Backend (Documentação da API):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Postgres:** `localhost:5432`
- **Redis:** `localhost:6379`

## Fluxo Operacional

```mermaid
flowchart LR
  A[Cliente (Web/PWA)] --&gt; B[Frontend Next.js]
  B --&gt;|REST| C[Backend FastAPI]
  C --&gt;|DB| D[(PostgreSQL)]
  C --&gt;|Cache| E[(Redis)]
  C --&gt; F[Checkout]
  C --&gt; G[Orders]
  C --&gt; H[Catalog]
  C --&gt; I[Auth]
```

## Arquitetura Multi-tenant (MVP)

A abordagem inicial para multi-tenancy é baseada em **rotas**.

- **Frontend:** As rotas do Next.js usam um parâmetro dinâmico `[tenant]` para identificar a pizzaria.
  - Painel do Cliente: `/(client)/[tenant]/...`
  - Site Público: `/(public)/[tenant]/...`
- **Backend:** A API identifica o tenant através de um header `X-Tenant` (enviado pelo frontend) ou extraindo-o do path da URL. No futuro, a lógica de banco de dados usará **Row-Level Security (RLS)** no PostgreSQL para isolar os dados de forma segura e automática.

## Endpoints Principais (MVP)

- `POST /api/auth/login`: Autentica um usuário e retorna um token JWT.
- `POST /api/checkout`: Cria uma nova sessão de checkout com os itens do carrinho.
- `GET /api/orders`: Lista os pedidos para um tenant.

## Estrutura de Pastas

```
meu-pedaco-favorito/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── models/
│   │   └── schemas/
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
└── frontend/
    ├── app/
    ├── components/
    ├── lib/
    ├── public/
    ├── next.config.mjs
    ├── package.json
    ├── Dockerfile
    └── .env.example
```

## Backlog Curto

- [ ] Persistir pedidos reais (SQLAlchemy + Alembic)
- [ ] CRUD de sabores
- [ ] Autenticação JWT real
- [ ] Checkout com pagamento simulado
- [ ] Tema por tenant
- [ ] RLS e subdomínio por tenant (fase 2)

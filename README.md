# Music Stems Platform

Plataforma web brasileira de separação musical em 6 stems:
- voz
- bateria
- baixo
- guitarra
- piano
- outros

## Stack inicial
- web: Next.js
- api: FastAPI
- worker: Python
- banco: PostgreSQL
- fila: Redis

## Estrutura inicial
- apps/web
- services/api
- services/worker
- docs

## Estrutura do monorepo
```text
.
├── apps/
│   └── web/          # Next.js + TypeScript
├── services/
│   ├── api/          # FastAPI + dominio conceitual inicial
│   └── worker/       # Worker Python + config basica
├── docker-compose.yml
├── Makefile
└── README.md
```

## Objetivo
Construir um MVP web focado no mercado brasileiro, com:
- processamento em 6 stems
- planos Free / Solo / Pro
- preço em reais
- PIX

## Escopo atual
Esta etapa prepara a base tecnica do monorepo sem implementar:
- billing
- autenticação
- processamento de áudio
- fila real
- storage real

## Pré-requisitos
- Node.js 24 LTS
- npm 10+
- Python 3.11+
- Docker + Docker Compose

## Setup local
1. Copie o arquivo de ambiente raiz:
   ```bash
   cp .env.example .env
   ```
2. Suba PostgreSQL e Redis:
   ```bash
   make up
   ```
3. Instale as dependências do front-end:
   ```bash
   make web-install
   ```
4. Prepare o ambiente da API:
   ```bash
   make api-install
   ```
5. Prepare o ambiente do worker:
   ```bash
   make worker-install
   ```
6. Copie os ambientes dos serviços:
   ```bash
   cp services/api/.env.example services/api/.env
   cp services/worker/.env.example services/worker/.env
   ```

## Executando os serviços
### Web
```bash
make web-dev
```

### API
```bash
make api-run
```

Rotas iniciais disponíveis:
- `GET /` retorna metadados básicos da aplicação
- `GET /health` retorna o status simples da API

Documentação automática:
- `http://localhost:8000/docs`

### Worker
```bash
make worker-run
```

## Infra local
O `docker-compose.yml` sobe apenas a infraestrutura compartilhada neste momento:
- PostgreSQL em `localhost:5432`
- Redis em `localhost:6379`

Para acompanhar logs ou encerrar os containers:
```bash
make logs
make down
```

## Base preparada para a próxima etapa
- Configuração da API centralizada em `services/api/app/core/settings.py`
- Rotas de sistema isoladas em `services/api/app/api/routes/system.py`
- Modelos ORM em `services/api/app/domain/models.py`
- Schemas de domínio em `services/api/app/domain/schemas.py`
- Infra de banco em `services/api/app/db/`
- Alembic configurado em `services/api/alembic/`
- Configuração do worker centralizada em `services/worker/app/core/settings.py`

## Banco e migrations
Depois de copiar `services/api/.env.example` para `services/api/.env`, a API passa a usar `DATABASE_URL` com `SQLAlchemy 2.x` e PostgreSQL como alvo principal.

Aplicar a migration inicial:
```bash
make api-db-upgrade
```

Ver estado atual e histórico:
```bash
make api-db-current
make api-db-history
```

Criar uma nova migration autogerada:
```bash
make api-db-revision MESSAGE="descricao_curta"
```

Voltar a última migration:
```bash
make api-db-downgrade
```

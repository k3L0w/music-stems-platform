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
│   ├── api/          # FastAPI
│   └── worker/       # Worker Python
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
Este scaffolding prepara a base do monorepo sem implementar:
- billing
- autenticação
- processamento de áudio

## Pré-requisitos
- Node.js 20+
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

## Executando os serviços
### Web
```bash
cd apps/web
npm run dev
```

### API
```bash
cd services/api
cp .env.example .env
. .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Worker
```bash
cd services/worker
cp .env.example .env
. .venv/bin/activate
python -m app.main
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

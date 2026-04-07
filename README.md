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

Para conectar o web local na API local, use a URL padrao `http://127.0.0.1:8000` ou defina:
```bash
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### API
```bash
make api-run
```

Rotas iniciais disponíveis:
- `GET /` retorna metadados básicos da aplicação
- `GET /health` retorna o status simples da API
- `GET /plans` lista planos cadastrados no banco
- `GET /projects` lista projetos, com filtro opcional por `user_id`
- `GET /projects/{project_id}` busca um projeto por id
- `POST /projects` cria um projeto
- `PATCH /projects/{project_id}` atualiza campos básicos do projeto
- `POST /projects/{project_id}/upload-target` gera um alvo de upload mockado
- `POST /projects/{project_id}/upload-complete` confirma upload concluído
- `POST /projects/{project_id}/jobs` cria um job de processamento
- `GET /projects/{project_id}/jobs` lista jobs de um projeto
- `GET /jobs/{job_id}` consulta um job por id
- `PATCH /jobs/{job_id}/status` atualiza manualmente o status de um job
- `GET /projects/{project_id}/stems` lista stems gerados de um projeto
- `GET /stems/{stem_id}` consulta um stem por id
- `POST /stems/{stem_id}/download-target` gera um download target mockado para um stem
- `GET /projects/{project_id}/download-targets` lista download targets mockados dos stems do projeto
- `DELETE /projects/{project_id}` remove um projeto

Documentação automática:
- `http://localhost:8000/docs`

### Worker
```bash
make worker-run
```

O worker agora roda em loop simples, busca jobs com status `queued` no banco e faz a transicao automatica para `running` e depois `succeeded`, gerando stems placeholder ao final.

Configuracoes locais uteis em `services/worker/.env`:
```bash
WORKER_POLLING_INTERVAL_SECONDS=2
WORKER_PROCESSING_DELAY_SECONDS=3
```

Na tela de detalhe do projeto, os stems gerados passam a exibir links mockados de download retornados pela API.

Criacao de jobs agora respeita limites basicos por plano:
- `free`: ate 2 stems por job e ate 1 job ativo por vez
- `solo`: ate 4 stems por job e ate 2 jobs ativos por vez
- `pro`: ate 6 stems por job e ate 5 jobs ativos por vez

Para esse MVP, job ativo significa status `queued` ou `running`. Quando um limite de plano e excedido, a API responde com `409 Conflict` e mensagem clara.

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

## Uso rápido da API
Listar planos:
```bash
curl http://localhost:8000/plans
```

Popular planos básicos para teste local:
```bash
docker compose exec -T postgres psql -U music_stems -d music_stems < services/api/scripts/seed_plans.sql
```

Criar projeto:
```bash
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "00000000-0000-0000-0000-000000000001",
    "name": "Meu primeiro projeto",
    "source_filename": "musica.wav",
    "source_content_type": "audio/wav",
    "source_size_bytes": 10485760
  }'
```

Criar job para um projeto:
```bash
curl -X POST http://localhost:8000/projects/PROJECT_ID/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "htdemucs_6s",
    "requested_stems": ["vocals", "drums", "bass"]
  }'
```

Gerar upload target mockado:
```bash
curl -X POST http://localhost:8000/projects/PROJECT_ID/upload-target
```

Gerar download target mockado de um stem:
```bash
curl -X POST http://localhost:8000/stems/STEM_ID/download-target
```

Listar download targets mockados de um projeto:
```bash
curl http://localhost:8000/projects/PROJECT_ID/download-targets
```

Confirmar upload concluído:
```bash
curl -X POST http://localhost:8000/projects/PROJECT_ID/upload-complete \
  -H "Content-Type: application/json" \
  -d '{
    "object_key": "projects/PROJECT_ID/source/musica.wav",
    "source_filename": "musica.wav",
    "source_content_type": "audio/wav",
    "source_size_bytes": 10485760
  }'
```

Listar jobs de um projeto:
```bash
curl http://localhost:8000/projects/PROJECT_ID/jobs
```

Consultar job por id:
```bash
curl http://localhost:8000/jobs/JOB_ID
```

Atualizar status de um job:
```bash
curl -X PATCH http://localhost:8000/jobs/JOB_ID/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "succeeded"
  }'
```

Listar stems de um projeto:
```bash
curl http://localhost:8000/projects/PROJECT_ID/stems
```

Consultar stem por id:
```bash
curl http://localhost:8000/stems/STEM_ID
```

## Uso rapido do web
Com a API rodando em `http://127.0.0.1:8000`, abra o front em `http://localhost:3000`.

Fluxo principal disponivel pela interface:
- listar projetos
- criar projeto
- gerar upload target mockado
- confirmar upload completo
- criar job
- atualizar status de job
- visualizar stems do projeto

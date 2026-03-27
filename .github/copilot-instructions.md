# Instruções do repositório

## Objetivo do projeto
Este repositório implementa uma plataforma web brasileira de separação musical em 6 stems:
- vocals
- drums
- bass
- guitar
- piano
- other

## Stack oficial
- Front-end: Next.js + TypeScript
- API: FastAPI + Python
- Worker: Python
- Banco: PostgreSQL
- Fila/cache: Redis
- Processamento de áudio: htdemucs_6s
- Storage: S3 compatível ou equivalente
- Infra local: Docker Compose

## Regras de implementação
- Sempre apresentar um plano antes de editar muitos arquivos.
- Fazer mudanças pequenas e incrementais.
- Não alterar billing sem testes.
- Não alterar autenticação sem revisão manual.
- Não expor arquivos privados publicamente.
- Toda alteração no worker deve incluir logs e métricas.
- Não mudar schema sem migration.
- Respeitar separação entre web, api e worker.

## Qualidade
- Priorizar código simples, legível e modular.
- Criar testes para regras críticas.
- Evitar dependências desnecessárias.
- Não inventar regras de negócio não especificadas.

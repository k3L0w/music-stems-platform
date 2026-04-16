#!/bin/bash

set -e

echo "🚀 Iniciando ambiente Music Stems Platform..."

PROJECT_ROOT=~/Documents/music-stems-platform

cd $PROJECT_ROOT

echo "📦 Subindo infraestrutura (Postgres + Redis)..."
sudo docker compose up -d

echo "⏳ Aguardando banco ficar disponível..."
sleep 3

echo "🔍 Verificando Postgres..."
sudo docker compose exec postgres pg_isready || true

echo "🐍 Ativando ambiente Python..."
cd services/api
source .venv/bin/activate

echo "📚 Instalando dependências (se necessário)..."
pip install -r requirements.txt > /dev/null

echo "🧱 Aplicando migrations..."
alembic upgrade head

echo "🔥 Subindo API..."
gnome-terminal -- bash -c "cd $PROJECT_ROOT/services/api && source .venv/bin/activate && uvicorn app.main:app --reload; exec bash"

echo "🌐 Subindo Frontend..."
gnome-terminal -- bash -c "cd $PROJECT_ROOT/apps/web && npm run dev; exec bash"

echo "✅ Ambiente iniciado com sucesso!"
echo ""
echo "🔗 Frontend: http://localhost:3000"
echo "🔗 API: http://localhost:8000/docs"

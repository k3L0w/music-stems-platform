#!/bin/bash

set -e

echo "💣 Resetando ambiente completamente..."

PROJECT_ROOT=~/Documents/music-stems-platform

cd $PROJECT_ROOT

echo "🧹 Derrubando containers + volumes..."
sudo docker compose down -v

echo "🚀 Subindo novamente..."
sudo docker compose up -d

echo "🐍 Ativando ambiente Python..."
cd services/api
source .venv/bin/activate

echo "🧱 Recriando schema..."
alembic upgrade head

echo "🔥 Subindo API..."
gnome-terminal -- bash -c "cd $PROJECT_ROOT/services/api && source .venv/bin/activate && uvicorn app.main:app --reload; exec bash"

echo "🌐 Subindo Frontend..."
gnome-terminal -- bash -c "cd $PROJECT_ROOT/apps/web && npm run dev; exec bash"

echo "✅ Ambiente resetado com sucesso!"

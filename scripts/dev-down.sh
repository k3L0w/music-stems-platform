#!/bin/bash

echo "🛑 Encerrando ambiente..."

PROJECT_ROOT=~/Documents/music-stems-platform

echo "🔪 Matando processos do frontend e backend..."
pkill -f uvicorn || true
pkill -f "npm run dev" || true

echo "🐳 Derrubando containers..."
cd $PROJECT_ROOT
sudo docker compose down

echo "✅ Ambiente encerrado."

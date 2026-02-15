#!/bin/bash
# Script de inicialização para configurar o ambiente EstatiCar Docker
# Usage: ./docker-setup.sh [modelo-ollama]

set -e

MODELO=${1:-mistral}

echo "🐳 EstatiCar Docker Setup"
echo "========================="
echo ""

# Detectar se usa Docker ou Podman
CONTAINER_CMD="docker"
if docker info > /dev/null 2>&1; then
    echo "✓ Docker detectado"
elif podman info > /dev/null 2>&1; then
    CONTAINER_CMD="podman"
    echo "✓ Podman detectado"
else
    echo "❌ Nem Docker nem Podman estão rodando. Por favor, inicie um deles e tente novamente."
    exit 1
fi

echo ""

# Verificar se o compose está disponível
if ! $CONTAINER_CMD compose version > /dev/null 2>&1; then
    echo "❌ $CONTAINER_CMD compose não está disponível."
    exit 1
fi

echo "✓ $CONTAINER_CMD compose está disponível"
echo ""

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
cd app
mkdir -p uploads
mkdir -p build_assets
echo "  ✓ Diretórios criados"

# Limpar containers antigos e reconstruir
echo ""
echo "🧹 Limpando containers antigos..."
$CONTAINER_CMD compose down

echo ""
echo "🔨 Reconstruindo imagem..."
$CONTAINER_CMD compose build --no-cache

echo ""
echo "📦 Iniciando serviços..."
$CONTAINER_CMD compose up -d

echo ""
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Verificar se os serviços estão rodando
if ! $CONTAINER_CMD compose ps | grep -q "Up"; then
    echo "❌ Erro ao iniciar serviços. Verifique os logs:"
    $CONTAINER_CMD compose logs --tail=50
    exit 1
fi

echo "✓ Serviços iniciados"
echo ""

# Baixar modelo Ollama
echo "🤖 Baixando modelo Ollama: $MODELO"
echo "   (Isso pode demorar alguns minutos na primeira vez...)"
$CONTAINER_CMD exec -it ollama ollama pull $MODELO

echo ""
echo "✓ Modelo $MODELO baixado com sucesso"
echo ""

# Mostrar modelos instalados
echo "📋 Modelos Ollama instalados:"
$CONTAINER_CMD exec -it ollama ollama list

echo ""
echo "✅ Setup concluído!"
echo ""
echo "🌐 Acesse a aplicação em: http://localhost:8080"
echo ""
echo "📊 Serviços disponíveis:"
echo "   - EstatiCar Web:  http://localhost:8080"
echo "   - Downloads:      http://localhost:8081"
echo "   - Qdrant API:     http://localhost:6333"
echo "   - Ollama API:     http://localhost:11434"
echo ""
echo "📝 Comandos úteis:"
echo "   - Ver logs:       $CONTAINER_CMD compose logs -f"
echo "   - Parar:          $CONTAINER_CMD compose down"
echo "   - Reiniciar:      $CONTAINER_CMD compose restart"
echo ""

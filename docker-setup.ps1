# Script de inicialização para configurar o ambiente FlechaSQL Docker (Windows)
# Usage: .\docker-setup.ps1 [modelo-ollama]

param(
    [string]$Modelo = "mistral"
)

Write-Host "🐳 FlechaSQL Docker Setup" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Detectar se usa Docker ou Podman
$containerCmd = "docker"
try {
    docker info | Out-Null
    Write-Host "✓ Docker detectado" -ForegroundColor Green
} catch {
    try {
        podman info | Out-Null
        $containerCmd = "podman"
        Write-Host "✓ Podman detectado" -ForegroundColor Green
    } catch {
        Write-Host "❌ Nem Docker nem Podman estão rodando. Por favor, inicie um deles e tente novamente." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Verificar se o compose está disponível
try {
    & $containerCmd compose version | Out-Null
    Write-Host "✓ $containerCmd compose está disponível" -ForegroundColor Green
} catch {
    Write-Host "❌ $containerCmd compose não está disponível." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Criar diretórios necessários
Write-Host "📁 Criando diretórios necessários..." -ForegroundColor Yellow
Set-Location app
if (-not (Test-Path "uploads")) {
    New-Item -ItemType Directory -Path "uploads" | Out-Null
    Write-Host "  ✓ Diretório uploads criado" -ForegroundColor Green
}
if (-not (Test-Path "build_assets")) {
    New-Item -ItemType Directory -Path "build_assets" | Out-Null
    Write-Host "  ✓ Diretório build_assets criado" -ForegroundColor Green
}

# Limpar containers antigos e reconstruir
Write-Host ""
Write-Host "🧹 Limpando containers antigos..." -ForegroundColor Yellow
& $containerCmd compose down

Write-Host ""
Write-Host "🔨 Reconstruindo imagem..." -ForegroundColor Yellow
& $containerCmd compose build --no-cache

Write-Host ""
Write-Host "📦 Iniciando serviços..." -ForegroundColor Yellow
& $containerCmd compose up -d

Write-Host ""
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar se os serviços estão rodando
$services = & $containerCmd compose ps
if ($services -notmatch "Up") {
    Write-Host "❌ Erro ao iniciar serviços. Verifique os logs:" -ForegroundColor Red
    & $containerCmd compose logs --tail=50
    exit 1
}

Write-Host "✓ Serviços iniciados" -ForegroundColor Green
Write-Host ""

# Baixar modelo Ollama
Write-Host "🤖 Baixando modelo Ollama: $Modelo" -ForegroundColor Yellow
Write-Host "   (Isso pode demorar alguns minutos na primeira vez...)" -ForegroundColor Yellow
& $containerCmd exec -it ollama ollama pull $Modelo

Write-Host ""
Write-Host "✓ Modelo $Modelo baixado com sucesso" -ForegroundColor Green
Write-Host ""

# Mostrar modelos instalados
Write-Host "📋 Modelos Ollama instalados:" -ForegroundColor Cyan
& $containerCmd exec -it ollama ollama list

Write-Host ""
Write-Host "✅ Setup concluído!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesse a aplicação em: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Serviços disponíveis:" -ForegroundColor Cyan
Write-Host "   - FlechaSQL Web:  http://localhost:8080"
Write-Host "   - Downloads:      http://localhost:8081"
Write-Host "   - Qdrant API:     http://localhost:6333"
Write-Host "   - Ollama API:     http://localhost:11434"
Write-Host ""
Write-Host "📝 Comandos úteis:" -ForegroundColor Cyan
Write-Host "   - Ver logs:       $containerCmd compose logs -f"
Write-Host "   - Parar:          $containerCmd compose down"
Write-Host "   - Reiniciar:      $containerCmd compose restart"
Write-Host ""

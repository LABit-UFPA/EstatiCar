#!/usr/bin/env pwsh
# Script para verificar conectividade e health dos containers EstatiCar

param(
    [string]$ContainerRuntime = "auto"  # auto, docker, ou podman
)

Write-Host "🔍 EstatiCar - Verificação de Saúde dos Containers" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Detectar runtime
$cmd = "docker"
if ($ContainerRuntime -eq "podman") {
    $cmd = "podman"
} elseif ($ContainerRuntime -eq "auto") {
    try {
        docker info | Out-Null
        $cmd = "docker"
    } catch {
        try {
            podman info | Out-Null
            $cmd = "podman"
        } catch {
            Write-Host "❌ Nem Docker nem Podman encontrados!" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host "Usando: $cmd" -ForegroundColor Yellow
Write-Host ""

# Verificar containers rodando
Write-Host "📦 Status dos Containers:" -ForegroundColor Cyan
& $cmd ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" --filter "name=estaticar" --filter "name=qdrant" --filter "name=ollama"
Write-Host ""

# Verificar health do Qdrant
Write-Host "🔍 Testando Qdrant..." -ForegroundColor Yellow
try {
    $qdrantHealth = & $cmd exec qdrant wget -q -O- http://localhost:6333/health 2>$null
    if ($qdrantHealth -match "ok|healthy") {
        Write-Host "  ✅ Qdrant está saudável" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Qdrant respondeu mas status desconhecido" -ForegroundColor Yellow
        Write-Host "     Resposta: $qdrantHealth"
    }
} catch {
    Write-Host "  ❌ Qdrant não está respondendo" -ForegroundColor Red
}

# Verificar Ollama
Write-Host "🤖 Testando Ollama..." -ForegroundColor Yellow
try {
    $ollamaList = & $cmd exec ollama ollama list 2>$null
    if ($ollamaList) {
        Write-Host "  ✅ Ollama está rodando" -ForegroundColor Green
        Write-Host "     Modelos instalados:" -ForegroundColor Cyan
        & $cmd exec ollama ollama list | Select-Object -Skip 1 | ForEach-Object {
            Write-Host "       - $_" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ⚠️  Ollama está rodando mas sem modelos" -ForegroundColor Yellow
        Write-Host "     Execute: $cmd exec -it ollama ollama pull mistral"
    }
} catch {
    Write-Host "  ❌ Ollama não está respondendo" -ForegroundColor Red
}

# Testar conectividade entre containers
Write-Host ""
Write-Host "🌐 Testando Conectividade Interna:" -ForegroundColor Cyan

Write-Host "  EstatiCar → Qdrant..." -ForegroundColor Yellow
try {
    & $cmd exec estaticar wget -q -O- http://qdrant:6333/health -T 2 2>$null | Out-Null
    Write-Host "    ✅ Conectado" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Falha na conexão" -ForegroundColor Red
}

Write-Host "  EstatiCar → Ollama..." -ForegroundColor Yellow
try {
    & $cmd exec estaticar wget -q -O- http://ollama:11434 -T 2 2>$null | Out-Null
    Write-Host "    ✅ Conectado" -ForegroundColor Green
} catch {
    Write-Host "    ❌ Falha na conexão" -ForegroundColor Red
}

# Verificar rede
Write-Host ""
Write-Host "🔗 Informações da Rede:" -ForegroundColor Cyan
$networkName = & $cmd network ls --filter "name=estaticar" --format "{{.Name}}" | Select-Object -First 1
if ($networkName) {
    Write-Host "  Rede: $networkName" -ForegroundColor Gray
    Write-Host "  Containers conectados:" -ForegroundColor Gray
    & $cmd network inspect $networkName --format '{{range $key, $value := .Containers}}  - {{$value.Name}} ({{$value.IPv4Address}}){{"\n"}}{{end}}'
} else {
    Write-Host "  ⚠️  Rede estaticar não encontrada" -ForegroundColor Yellow
}

# Verificar logs recentes
Write-Host ""
Write-Host "📋 Últimas 5 linhas de log do EstatiCar:" -ForegroundColor Cyan
& $cmd logs estaticar --tail=5 2>&1 | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Para mais detalhes: $cmd compose logs -f" -ForegroundColor Yellow
Write-Host "Interface web: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""

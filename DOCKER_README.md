# 🐳 Executando EstatiCar com Docker/Podman

Este guia mostra como executar a aplicação EstatiCar usando containers Docker ou Podman.

## 📋 Pré-requisitos

- Docker **ou** Podman
- Docker Compose **ou** Podman Compose

> **Nota**: Os scripts de setup detectam automaticamente se você está usando Docker ou Podman.

## 🚀 Início Rápido

### 1. Iniciar os serviços

**Opção A - Script Automático (Recomendado)**:

```bash
# Windows (PowerShell)
.\docker-setup.ps1

# Linux/Mac
chmod +x docker-setup.sh
./docker-setup.sh
```

**Opção B - Manual**:

No diretório `app/`, execute (substituindo `docker` por `podman` se necessário):

```bash
# Criar diretórios necessários primeiro
mkdir -p uploads build_assets

# Subir os containers
docker compose up -d
# ou
podman compose up -d
```

Isso iniciará três serviços em uma rede isolada (`estaticar-network`):
- **estaticar**: A aplicação principal (portas 8080 e 8081)
- **qdrant**: Banco de dados vetorial (porta 6333)
- **ollama**: Servidor LLM (porta 11434)

Os serviços usam **health checks** para garantir que Qdrant e Ollama estejam prontos antes de iniciar a aplicação.

### 2. Baixar um modelo Ollama

Antes de usar a aplicação, você precisa baixar um modelo LLM no container Ollama:

```bash
docker exec -it ollama ollama pull mistral
# ou
podman exec -it ollama ollama pull mistral
```

Ou outro modelo de sua preferência (ex: `llama2`, `llama3`, `codellama`, `phi`, `qwen`).

> **Dica**: Use `docker exec -it ollama ollama list` para ver os modelos disponíveis localmente.

### 3. Acessar a aplicação

Abra seu navegador em:
- **Interface Web**: http://localhost:8080

## 🔧 Comandos Úteis

> **Nota**: Nos exemplos abaixo, substitua `docker` por `podman` se estiver usando Podman.

### Ver logs

```bash
# Todos os serviços
docker compose logs -f

# Apenas a aplicação
docker compose logs -f estaticar

# Apenas o Ollama
docker compose logs -f ollama
```

### Parar os serviços

```bash
docker compose down
```

### Parar e remover volumes (dados)

```bash
docker compose down -v
```

### Reconstruir a imagem

```bash
docker compose build --no-cache
docker compose up -d
```

## 🎮 Gerenciar modelos Ollama

### Listar modelos instalados

```bash
docker exec -it ollama ollama list
```

### Baixar um modelo

```bash
docker exec -it ollama ollama pull <nome-do-modelo>
```

### Remover um modelo

```bash
docker exec -it ollama ollama rm <nome-do-modelo>
```

### Testar um modelo

```bash
docker exec -it ollama ollama run mistral "Hello, how are you?"
```

## 📂 Volumes e Persistência

Os seguintes dados são persistidos em volumes Docker:

- **qdrant_storage**: Dados do banco vetorial (embeddings, treinamento)
- **ollama_data**: Modelos LLM baixados

Os seguintes dados são mapeados para o host:

- **app/build_assets**: Configurações e dados da aplicação
- **app/uploads**: Arquivos enviados via interface

## 🖥️ GPU Support (Opcional)

Se você tem uma GPU NVIDIA, pode habilitar aceleração GPU para o Ollama:

1. Instale o [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

2. No arquivo `compose.yml`, descomente as linhas da seção `deploy` do serviço `ollama`:

```yaml
ollama:
  # ...
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

3. Reinicie os containers:

```bash
docker compose down
docker compose up -d
```

## 🔍 Troubleshooting

### Erro "no such file or directory" ao montar volumes

Se você ver um erro como `statfs /mnt/c/Users/.../uploads: no such file or directory`:

```bash
# Criar os diretórios necessários
cd app
mkdir -p uploads build_assets

# Tentar novamente
podman compose up -d
```

Os scripts automáticos (`docker-setup.ps1` / `docker-setup.sh`) já criam esses diretórios automaticamente.

### Erro "No module named flet.__main__"

Este erro ocorre quando há conflito entre o código no container e os volume mounts. Para corrigir:

```bash
# Parar e remover o container
podman stop estaticar
podman rm estaticar

# Reconstruir a imagem
cd app
podman compose build --no-cache

# Iniciar novamente
podman compose up -d
```

**Nota importante**: O arquivo `compose.yml` não monta o diretório de código fonte (`../app`) por padrão para evitar conflitos com as dependências instaladas no container. Se você precisa fazer desenvolvimento com hot-reload, veja a seção "Modo Desenvolvimento" abaixo.

### A aplicação não conecta ao Qdrant

Verifique se o serviço está rodando:
```bash
docker compose ps
curl http://localhost:6333/collections
```

### A aplicação não encontra o modelo Ollama

1. Verifique se o modelo está instalado:
   ```bash
   docker exec -it ollama ollama list
   ```

2. Baixe o modelo necessário:
   ```bash
   docker exec -it ollama ollama pull mistral
   ```

### Erro de porta já em uso

Se as portas 8080, 8081, 6333 ou 11434 já estiverem em uso, você pode alterá-las no `compose.yml`:

```yaml
services:
  estaticar:
    ports:
      - "9080:8080"  # Altere 9080 para a porta desejada
      - "9081:8081"
```

### Verificar conectividade entre containers

Para testar se os containers conseguem se comunicar na rede:

```bash
# Verificar se Qdrant está acessível
docker exec -it estaticar wget -q -O- http://qdrant:6333/health

# Verificar se Ollama está acessível
docker exec -it estaticar nc -zv ollama 11434

# Ver todas as redes
docker network ls

# Inspecionar a rede estaticar
docker network inspect app_estaticar-network
```

## 📝 Variáveis de Ambiente

As seguintes variáveis podem ser configuradas no `compose.yml`:

- `QDRANT_URL`: URL do serviço Qdrant (padrão: `http://qdrant:6333`)
- `OLLAMA_HOST`: URL do serviço Ollama (padrão: `http://ollama:11434`)
- `PYTHONUNBUFFERED`: Modo de logging Python (padrão: `1`)

## 🛠️ Modo Desenvolvimento

Por padrão, o código da aplicação fica dentro do container para evitar conflitos com dependências. Se você precisa fazer alterações no código com hot-reload:

1. Edite o arquivo `compose.yml` e descomente a linha de volume mount:

```yaml
volumes:
  - ../app:/app/app  # Descomente esta linha
  - ./build_assets:/app/app/build_assets
  - ./uploads:/app/app/uploads
```

2. Reconstrua e reinicie:

```bash
podman compose down
podman compose build --no-cache
podman compose up -d
```

**Aviso**: Montar o diretório do código pode sobrescrever as dependências instaladas. Use apenas durante desenvolvimento.

## 🏗️ Arquitetura

Os containers estão conectados em uma rede bridge isolada (`estaticar-network`):

```
┌─────────────────────────────────────────────────────┐
│         estaticar-network (bridge)                  │
│                                                     │
│  ┌─────────────┐                                   │
│  │  Navegador  │ (host)                            │
│  └──────┬──────┘                                   │
│         │ :8080 (web) / :8081 (downloads)          │
│         │                                           │
│  ┌──────▼──────┐                                   │
│  │  EstatiCar  │                                   │
│  │  Container  │                                   │
│  └──┬────────┬─┘                                   │
│     │        │                                      │
│     │:6333   │:11434                               │
│     │        │                                      │
│  ┌──▼──────┐ │                                     │
│  │ Qdrant  │ │  Health checks:                     │
│  │(Vector) │ │  - Qdrant: wget health endpoint     │
│  └─────────┘ │  - Ollama: ollama list              │
│              │                                      │
│        ┌─────▼────┐                                │
│        │  Ollama  │                                │
│        │   (LLM)  │                                │
│        └──────────┘                                │
│                                                     │
└─────────────────────────────────────────────────────┘

Volumes Persistentes:
  - qdrant_storage  → Embeddings e dados vetoriais
  - ollama_data     → Modelos LLM baixados
```

### Benefícios da Rede Isolada

- **Isolamento**: Os containers se comunicam apenas entre si
- **DNS interno**: Resolvem-se por nome (qdrant, ollama, estaticar)
- **Segurança**: Sem exposição desnecessária ao host
- **Health checks**: Aplicação só inicia quando dependências estão prontas

## 📜 Licença

Ver arquivo LICENSE no repositório principal.

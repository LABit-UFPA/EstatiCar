# EstatiCar

## ⚠️ Informações sobre as Branches

Este projeto possui duas versões ativas em desenvolvimento:

- **Branch `web`**: Versão web da aplicação
- **Branch `desktop`**: Versão desktop da aplicação

> **Nota:** A branch `main` está desatualizada no momento. Por favor, utilize as branches `web` ou `desktop` de acordo com sua necessidade.

---

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- **Python 3.8+**
- **Docker** e **Docker Compose**
- **Ollama** ([Instruções de instalação](https://ollama.ai))

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/kimlimalima/EstatiCar.git
cd EstatiCar
```

### 2. Escolha e mude para a branch desejada

```bash
# Para a versão desktop
git checkout desktop

# OU para a versão web
git checkout web
```

### 3. Instale as dependências Python

```bash
pip install flet vanna ollama qdrant-client
```

### 4. Inicie o Qdrant (banco de dados vetorial)

Navegue até a pasta do aplicativo e inicie o Docker Compose:

```bash
cd src/app
docker-compose up -d
```

Isso iniciará o Qdrant nas portas 6333 e 6334.

### 5. Configure o Ollama

Certifique-se de que o Ollama está rodando e baixe o modelo necessário:

```bash
ollama pull llama2
```

### 6. Execute a aplicação

```bash
python main.py
```

---

## 🔧 Build do Executável (Opcional)

Para gerar um executável standalone:

```bash
pip install pyinstaller
pyinstaller build.spec
```

O executável será gerado na pasta `dist/`.

---

## 🛑 Parar os Serviços

Para parar o Qdrant:

```bash
docker-compose down
```

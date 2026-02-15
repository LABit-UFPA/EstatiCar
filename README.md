# EstatiCar 🎯

Uma aplicação web intuitiva para consultar bancos de dados SQLite usando linguagem natural, powered by AI.

## 📋 Características

- 🤖 Consultas em linguagem natural usando modelos LLM (via Ollama)
- 🗄️ Suporte a bancos de dados SQLite
- 📊 Visualização de resultados em tabelas interativas
- 💾 Exportação de resultados (Excel, CSV)
- 🎓 Treinamento do modelo com queries customizadas
- 🌐 Interface web moderna usando Flet
- 🐳 Suporte a containers Docker

## 🚀 Instalação e Execução

### Opção 1: Docker (Recomendado)

A forma mais fácil de rodar a aplicação é usando Docker:

```bash
# Windows (PowerShell)
.\docker-setup.ps1

# Linux/Mac
chmod +x docker-setup.sh
./docker-setup.sh
```

Acesse a aplicação em: http://localhost:8080

Para mais detalhes, veja [DOCKER_README.md](DOCKER_README.md)

### Opção 2: Desenvolvimento Local

#### Pré-requisitos

- Python 3.12+
- [Ollama](https://ollama.ai/) instalado e rodando
- [Qdrant](https://qdrant.tech/) rodando (ou via Docker)

#### Instalação

```bash
# Instalar dependências
pip install -e .

# Ou usando uv
uv pip install -e .

# Iniciar Qdrant (Docker)
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Iniciar Ollama e baixar um modelo
ollama pull mistral

# Executar a aplicação
cd app
python main.py
```

## 🏗️ Arquitetura

O projeto segue Clean Architecture com três camadas principais:

```
domain/          # Entidades e casos de uso (regras de negócio)
├── entities/    # Objetos de domínio
├── ports/       # Interfaces (abstrações)
└── use_cases/   # Lógica de negócio

infrastructure/  # Implementações concretas
├── adapters/    # Adaptadores para serviços externos
└── config/      # Configuração e I/O

presentation/    # Interface do usuário
├── components/  # Componentes visuais reutilizáveis
├── controllers/ # Controladores de eventos
├── views/       # Views da aplicação
├── state/       # Gerenciamento de estado
└── theme/       # Configuração de tema
```

## 📚 Tecnologias

- **[Flet](https://flet.dev/)**: Framework para criar aplicações web em Python
- **[Ollama](https://ollama.ai/)**: Servidor local de modelos LLM
- **[Vanna.ai](https://vanna.ai/)**: Framework para text-to-SQL
- **[Qdrant](https://qdrant.tech/)**: Banco de dados vetorial
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM Python
- **[Pandas](https://pandas.pydata.org/)**: Manipulação de dados

## 🎯 Como Usar

1. **Configurar Banco de Dados**: Selecione ou faça upload de um banco SQLite
2. **Treinar Modelo**: Adicione exemplos de queries SQL para melhorar a precisão
3. **Fazer Perguntas**: Digite perguntas em linguagem natural
4. **Visualizar Resultados**: Veja os dados em formato de tabela
5. **Exportar**: Salve os resultados em Excel ou CSV

## 🐳 Docker

Veja [DOCKER_README.md](DOCKER_README.md) para instruções detalhadas sobre como usar a versão containerizada.

## 📄 Licença

MIT License

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.


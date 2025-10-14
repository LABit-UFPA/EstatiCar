from vanna.ollama import Ollama
from vanna.qdrant import Qdrant_VectorStore

class OllamaService(Qdrant_VectorStore, Ollama):
    def __init__(self, config=None):
        Qdrant_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

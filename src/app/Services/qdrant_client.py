import platform
from qdrant_client import QdrantClient

if platform.system() == "Windows":
    from Services.start_qdrant_windows import StartQdrantWindows as QdrantManager
else:
    from Services.start_qdrant_linux import StartQdrantLinux as QdrantManager

qdrant = QdrantManager()
qdrant.start()

client = QdrantClient(url="http://localhost:6333")

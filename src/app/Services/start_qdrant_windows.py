import os
import sys
import subprocess
import psutil
from pathlib import Path

class StartQdrantWindows:
    def __init__(self):
        self.base_path = self.get_base_path()
        self.qdrant_path = self.base_path / "qdrant-x86_64-pc-windows-msvc/qdrant.exe"
        self.log_file = self.base_path / "qdrant.log"

    def get_base_path(self):
        """Retorna o diretório base (funciona tanto no .py quanto no .exe)."""
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        return Path(__file__).parent

    def is_qdrant_running(self):
        """Verifica se o qdrant.exe já está ativo."""
        for proc in psutil.process_iter(attrs=['name']):
            if "qdrant.exe" in proc.info['name'].lower():
                return True
        return False

    def start(self):
        """Inicia o Qdrant em background no Windows."""
        if not self.qdrant_path.exists():
            print(f"❌ Qdrant não encontrado em: {self.qdrant_path}")
            return

        if self.is_qdrant_running():
            print("⚙️  Qdrant já está rodando.")
            return

        with open(self.log_file, "a") as log:
            subprocess.Popen(
                [str(self.qdrant_path)],
                stdout=log,
                stderr=log,
                creationflags=subprocess.CREATE_NO_WINDOW  # evita abrir terminal
            )
        print(f"✅ Qdrant iniciado em background (logs em {self.log_file}).")

    def stop(self):
        """Encerra o processo qdrant.exe."""
        stopped = False
        for proc in psutil.process_iter(attrs=['name']):
            if "qdrant.exe" in proc.info['name'].lower():
                proc.terminate()
                stopped = True
                print("🛑 Qdrant encerrado.")
        if not stopped:
            print("⚙️  Nenhum processo Qdrant encontrado.")

if __name__ == "__main__":
    q = StartQdrantWindows()
    q.start()

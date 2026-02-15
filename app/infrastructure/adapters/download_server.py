"""Flask server for serving file downloads with proper headers."""

from flask import Flask, send_file, abort
import os
import threading
import logging


class DownloadServer:
    """Lightweight Flask server to serve download files."""
    
    def __init__(self, upload_dir: str, port: int = 8081):
        self.upload_dir = upload_dir
        self.port = port
        self.app = Flask(__name__)
        
        # Disable Flask logging except errors
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        self._setup_routes()
        self.server_thread = None
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/download/<filename>')
        def download_file(filename):
            """Serve file with download headers."""
            filepath = os.path.join(self.upload_dir, filename)
            
            print(f"[Flask] Requisição de download: {filename}")
            print(f"[Flask] Buscando arquivo em: {filepath}")
            
            if not os.path.exists(filepath):
                print(f"[Flask] ERRO: Arquivo não encontrado: {filepath}")
                print(f"[Flask] Arquivos disponíveis em {self.upload_dir}:")
                try:
                    for f in os.listdir(self.upload_dir):
                        print(f"  - {f}")
                except Exception as e:
                    print(f"[Flask] Erro ao listar diretório: {e}")
                abort(404)
            
            print(f"[Flask] Arquivo encontrado! Enviando: {filename}")
            
            # Send file with download headers (forces download in browser Downloads folder)
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    
    def start(self):
        """Start Flask server in background thread."""
        def run_server():
            print(f"[Flask] Download server iniciando na porta {self.port}")
            print(f"[Flask] Servindo arquivos de: {self.upload_dir}")
            print(f"[Flask] URL base: http://0.0.0.0:{self.port}/download/")
            # Listen on 0.0.0.0 to accept connections from outside container
            self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False, threaded=True)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Wait a bit for server to start
        import time
        time.sleep(0.5)
        print(f"[Flask] Servidor de download pronto!")

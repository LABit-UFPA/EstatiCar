"""Flask server for serving file downloads with proper headers."""

from flask import Flask, send_file, abort, after_this_request
import os
import threading
import logging
import time
from datetime import datetime, timedelta


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
        self.cleanup_thread = None
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/download/<filename>')
        def download_file(filename):
            """Serve file with download headers and delete after sending."""
            filepath = os.path.join(self.upload_dir, filename)
            
            print(f"[PROCESSING] Download request received: {filename}")
            print(f"[PROCESSING] Searching file at: {filepath}")
            
            if not os.path.exists(filepath):
                print(f"[ERROR] File not found: {filepath}")
                print(f"[PROCESSING] Available files in {self.upload_dir}:")
                try:
                    for f in os.listdir(self.upload_dir):
                        print(f"  - {f}")
                except Exception as e:
                    print(f"[ERROR] Failed to list directory: {e}")
                abort(404)
            
            print(f"[SUCCESS] File found, sending: {filename}")
            
            # Delete file after response is sent
            @after_this_request
            def cleanup_file(response):
                try:
                    # Small delay to ensure download completes
                    def delayed_delete():
                        time.sleep(2)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                            print(f"[SUCCESS] File deleted after download: {filename}")
                    
                    threading.Thread(target=delayed_delete, daemon=True).start()
                except Exception as e:
                    print(f"[ERROR] Failed to delete file {filename}: {e}")
                return response
            
            # Send file with download headers (forces download in browser Downloads folder)
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    
    def _cleanup_old_files(self, max_age_hours: int = 1):
        """Remove arquivos mais antigos que max_age_hours."""
        try:
            now = datetime.now()
            count = 0
            for filename in os.listdir(self.upload_dir):
                filepath = os.path.join(self.upload_dir, filename)
                if os.path.isfile(filepath):
                    # Check file age
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if now - file_time > timedelta(hours=max_age_hours):
                        os.remove(filepath)
                        count += 1
                        print(f"[SUCCESS] Removed old file: {filename}")
            
            if count > 0:
                print(f"[SUCCESS] {count} old file(s) removed")
        except Exception as e:
            print(f"[ERROR] Cleanup failed: {e}")
    
    def _periodic_cleanup(self, interval_minutes: int = 30, max_age_hours: int = 1):
        """Executa limpeza periódica de arquivos antigos."""
        while True:
            time.sleep(interval_minutes * 60)
            self._cleanup_old_files(max_age_hours)
    
    def start(self):
        """Start Flask server in background thread."""
        def run_server():
            print(f"[PROCESSING] Starting download server on port {self.port}")
            print(f"[PROCESSING] Serving files from: {self.upload_dir}")
            print(f"[PROCESSING] Base URL: http://0.0.0.0:{self.port}/download/")
            # Listen on 0.0.0.0 to accept connections from outside container
            self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False, threaded=True)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Start periodic cleanup thread (clean files older than 1 hour every 30 minutes)
        self.cleanup_thread = threading.Thread(
            target=self._periodic_cleanup, 
            args=(30, 1),  # Check every 30 min, remove files older than 1 hour
            daemon=True
        )
        self.cleanup_thread.start()
        
        # Wait a bit for server to start
        time.sleep(0.5)
        print(f"[SUCCESS] Download server ready")
        print(f"[PROCESSING] Auto-cleanup enabled (files > 1 hour will be removed)")

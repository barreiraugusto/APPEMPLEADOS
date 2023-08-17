import os
import subprocess
import sys
import threading
from pathlib import Path

proceso = None


class Server:
    def __init__(self):
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'udp_server_t.py')

    def try_connection(self, ):
        if proceso:
            proceso.kill()
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()

    def lanzar_servidor(self, var):
        global proceso
        ruta = self.ruta_server
        if var:
            proceso = subprocess.Popen([sys.executable, ruta])
            proceso.communicate()

    def stop_server(self, ):
        global proceso
        if proceso:
            proceso.kill()

import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)
import socketserver
from datetime import datetime

from app.orm import EmpleadoORM

global PORT


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        mensaje = data.decode('UTF-8')
        if mensaje == "control":
            respuesta = "conectado"
        else:
            print(f"{datetime.today()} - {mensaje}")
            try:
                empleado = EmpleadoORM.get(EmpleadoORM.id == mensaje)
                respuesta = empleado.nombre_completo()
            except EmpleadoORM.DoesNotExist:
                respuesta = "False"

        packed_data_2 = bytearray()
        packed_data_2 += respuesta.encode('utf-8')
        socket.sendto(packed_data_2, self.client_address)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()

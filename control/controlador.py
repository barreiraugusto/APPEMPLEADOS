"""
Modulo de Control de la App.

Esta aplicacion esta pensada para llevar el control de los datos de los empleados de una empresa.
"""
from tkinter import Tk

from comunicacion.cliente import UDPSender
from control.vista import Registro


class Controlador:
    """
    Está es la clase controlador de la app
    """

    def __init__(self, root):
        self.controlador = root
        self.vista = Registro(self.controlador)
        self.cliente = UDPSender("localhost", 9999)
        respuesta = self.cliente.send_value("Conectado!")
        print(respuesta)
        if respuesta == b'\xa0':
            self.vista.indicador_color.config(background="green")


if __name__ == "__main__":
    tkroot = Tk()
    app = Controlador(tkroot)
    tkroot.mainloop()

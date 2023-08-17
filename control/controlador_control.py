"""
Modulo de Control de la App.

Esta aplicacion esta pensada para llevar el control de los datos de los empleados de una empresa.
"""
import threading
import time
from tkinter import Tk

from comunicacion.cliente import UDPSender
from control.vista import Registro


class Controlador:
    """
    Está es la clase controlador de la app
    """

    def __init__(self, root):
        self.cliente = None
        self.controlador = root
        self.vista = Registro(self.controlador)
        self.vista.conectar()


if __name__ == "__main__":
    tkroot = Tk()
    app = Controlador(tkroot)
    tkroot.mainloop()

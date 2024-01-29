"""
Modulo de Control de la App.

Esta aplicacion esta pensada para llevar el control de los datos de los empleados de una empresa.
"""

from config import directorio_proyecto
from tkinter import Tk

from app.vista import Vista
from comunicacion.servidor import Server


class Controlador:
    """
    Está es la clase controlador de la app
    """

    def __init__(self, root):
        self.controlador = root
        self.vista = Vista(self.controlador)
        self.servidor = Server()
        self.servidor.try_connection()


if __name__ == "__main__":
    tkroot = Tk()
    app = Controlador(tkroot)
    tkroot.mainloop()

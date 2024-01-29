"""
Modulo de Control de la App.

Esta aplicacion esta pensada para llevar el control de los datos de los empleados de una empresa.
"""
from config import directorio_proyecto
from tkinter import Tk

from control.vista import Registro


class Controlador:
    """
    Está es la clase controlador de la app del control biometrico
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

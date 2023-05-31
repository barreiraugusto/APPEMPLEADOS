"""
Modulo de Control de la App.

Esta aplicacion esta pensada para llevar el control de los datos de los empleados de una empresa.
"""
from tkinter import Tk

from app.vista import Vista

if __name__ == "__main__":
    root = Tk()
    Vista(root)
    root.mainloop()

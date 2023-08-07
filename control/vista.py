"""
Interfaz grafica principal de la App
"""
from tkinter import Button, Frame, StringVar
from tkinter import ttk

from app.decoradores import registrar_info
from comunicacion.cliente import UDPSender


class Registro:
    def __init__(self, root):
        """
        Muestra la interfaz del simulador de lector biometrico.

        :param root: Ventana del lector.
        """
        self.root = root
        self.root.title("Lector biometrico")
        self.root.resizable(False, False)
        self.root.geometry("200x200")
        self.enviar = UDPSender("localhost", 9999)

        # DECLARACION DE VARIABLES DE TKINTER
        self.var_legajo = StringVar()

        # DECLARACION DE LOS FRAMES QUE SECTORIZAN EL ROOT
        self.frame_input = Frame(self.root)
        self.frame_input.grid(row=0, column=0, pady=10)

        self.frame_botones = Frame(self.root)
        self.frame_botones.grid(row=1, column=0, pady=10)

        # FRAME INPUTS
        self.label_legajo = ttk.Label(self.frame_input, text="Legajo: ")
        self.label_legajo.grid(row=0, column=0, padx=10, pady=10)
        self.entry_legajo = ttk.Entry(self.frame_input, textvariable=self.var_legajo, width=10)
        self.entry_legajo.grid(row=0, column=1, padx=10, pady=10)

        self.nombre = ttk.Label(self.frame_input, text="", width=10)
        self.nombre.grid(row=3, column=1, padx=10, pady=10)

        # FRAME BOTONES
        self.boton_entrar = Button(self.frame_botones, text="ENTRAR",
                                   command=lambda: self.entrar(self.var_legajo.get()))
        self.boton_entrar.grid(row=0, column=0, padx=10, pady=10)

        self.boton_salir = Button(self.frame_botones, text="SALIR", command=lambda: self.salir(self.var_legajo.get()))
        self.boton_salir.grid(row=0, column=1, padx=10, pady=10)

        self.indicador_color = ttk.Label(self.frame_input, background="red", width=2)
        self.indicador_color.grid(row=0, column=2, padx=5)

    @registrar_info
    def entrar(self, legajo):
        """
        Da entrada al turno.
        """
        texto = f"Entrada del empleado numero {legajo}"
        respuesta = self.enviar.send_value(texto)
        print(respuesta)
        return respuesta

    @registrar_info
    def salir(self, legajo):
        """
        Da salida del turno.
        """
        texto = f"Salida del empleado numero {legajo}"
        respuesta = self.enviar.send_value(texto)
        print(respuesta)
        return respuesta

"""
Interfaz grafica principal de la App
"""
import datetime
import os
import re
from tkinter import messagebox, Button, Frame, StringVar, PhotoImage, Menu
from tkinter import ttk

from peewee import IntegrityError
from tkcalendar import DateEntry

from app import observadores
from app.decoradores import registrar_info
from app.orm import EmpleadoORM
from comunicacion.servidor import Server
from app.empleado_registro import EmpleadoRegistro

class Vista:
    def __init__(self, root):
        """
        Muestra la interfaz proncipal de la app.

        :param root: Ventana principal de la app.
        """
        self.root = root
        self.root.title("ALTA Y BAJA DE PERSONAL")
        self.root.resizable(False, False)
        self.root.geometry("1230x550")
        self.root.overrideredirect(False)
        self.root.protocol("WM_DELETE_WINDOW", self.no_cerrar_ventana())

        try:
            ruta_icono = os.path.join(os.path.dirname(__file__), "img/icono.png")
            self.root.iconphoto(False, PhotoImage(file=ruta_icono))
        except:
            pass
        # DECLARACION DE VARIABLES DE TKINTER
        self.var_legajo = StringVar()
        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_cuil = StringVar()
        self.var_area = StringVar()
        self.var_sueldo = StringVar()
        # self.var_ingreso = StringVar()

        self.servidor = Server()

        # DECLARACION DE LOS FRAMES QUE SECTORIZAN EL ROOT
        self.frame_input = Frame(self.root)
        self.frame_input.grid(row=0, column=0, pady=10, sticky="ew")

        self.frame_botones = Frame(self.root)
        self.frame_botones.grid(row=1, column=0, pady=10, sticky="e")

        self.frame_tabla = Frame(self.root)
        self.frame_tabla.grid(row=2, column=0, sticky="ew")

        self.frame_footer = Frame(self.root)
        self.frame_footer.grid(row=3, column=0, pady=10, sticky="e")

        # MENU
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.apariencia = Menu(self.menubar, tearoff=0)
        self.apariencia.add_command(label="Oscuro", command=lambda: self.tema_oscuro())
        self.apariencia.add_command(label="Claro", command=lambda: self.tema_claro())
        self.menubar.add_cascade(label="Apariencia", menu=self.apariencia)

        # FRAME INPUTS
        self.label_legajo = ttk.Label(self.frame_input, text="N° de legajo")
        self.label_legajo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_legajo = ttk.Entry(
            self.frame_input, textvariable=self.var_legajo, width=30, state="readonly"
        )
        self.entry_legajo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_nombre = ttk.Label(self.frame_input, text="Nombre")
        self.label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_nombre = ttk.Entry(self.frame_input, textvariable=self.var_nombre, width=30)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.label_apellido = ttk.Label(self.frame_input, text="Apellido")
        self.label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.apellido = ttk.Entry(self.frame_input, textvariable=self.var_apellido, width=30)
        self.apellido.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.label_cuil = ttk.Label(self.frame_input, text="C.U.I.L.")
        self.label_cuil.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.cuil = ttk.Entry(self.frame_input, textvariable=self.var_cuil, width=30)
        self.cuil.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.label_area = ttk.Label(self.frame_input, text="Area")
        self.label_area.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.area = ttk.Entry(self.frame_input, textvariable=self.var_area, width=30)
        self.area.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        self.label_sueldo = ttk.Label(self.frame_input, text="Sueldo")
        self.label_sueldo.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.sueldo = ttk.Entry(self.frame_input, textvariable=self.var_sueldo, width=30)
        self.sueldo.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        self.ingreso = DateEntry(self.frame_input, width=12, background='darkblue', foreground='white',
                                 borderwidth=2)

        self.label_ingreso = ttk.Label(self.frame_input, text="Ingreso")
        self.label_ingreso.grid(row=2, column=2, padx=10, pady=10, sticky="w")
        self.ingreso.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        self.label_antiguedad = ttk.Label(self.frame_input, text="Antiguedad: ", width=30)
        self.label_antiguedad.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        self.label_vacaciones = ttk.Label(self.frame_input, text="Vacaciones: ", width=30)
        self.label_vacaciones.grid(row=1, column=4, padx=10, pady=10, sticky="w")
        self.label_pago_presentismo = ttk.Label(self.frame_input, text="Presentismo: ", width=30)
        self.label_pago_presentismo.grid(row=2, column=4, padx=10, pady=10, sticky="w")
        self.label_pago_antiguedad = ttk.Label(self.frame_input, text="Pago por Antiguedad: ", width=30)
        self.label_pago_antiguedad.grid(row=3, column=4, padx=10, pady=10, sticky="w")

        self.resultado_antiguedad = ttk.Label(self.frame_input, width=30)
        self.resultado_antiguedad.grid(row=0, column=5, padx=10, pady=10, sticky="w")
        self.resultado_vacaciones = ttk.Label(self.frame_input, text="", width=30)
        self.resultado_vacaciones.grid(row=1, column=5, padx=10, pady=10, sticky="w")
        self.resultado_pago_presentismo = ttk.Label(self.frame_input, text="", width=30)
        self.resultado_pago_presentismo.grid(row=2, column=5, padx=10, pady=10, sticky="w")
        self.resultado_pago_antiguedad = ttk.Label(self.frame_input, text="", width=30)
        self.resultado_pago_antiguedad.grid(row=3, column=5, padx=10, pady=10, sticky="w")

        # FRAME BOTONES

        self.boton_alta = Button(self.frame_botones, text="Alta", command=lambda: self.alta())
        self.boton_alta.grid(row=0, column=0, padx=10, pady=10)

        self.boton_baja = Button(self.frame_botones, text="Baja", command=lambda: self.baja())
        self.boton_baja.grid(row=0, column=1, padx=10, pady=10)

        self.boton_modificar = Button(self.frame_botones, text="Modificar", state="disabled",
                                      command=lambda: self.modificar())
        self.boton_modificar.grid(row=0, column=2, padx=10, pady=10)

        self.boton_ver_datos = Button(
            self.frame_botones,
            text="Ver datos",
            command=lambda: self.ver_datos())
        self.boton_ver_datos.grid(row=0, column=3, padx=10, pady=10)

        # FRAME self.tabla

        self.tabla = ttk.Treeview(self.frame_tabla)
        self.tabla["columns"] = (
            "NOMBRE",
            "APELLIDO",
            "AREA",
            "SUELDO",
            "C.U.I.L.",
            "INGRESO",
        )
        self.scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=self.scrollbar.set)

        self.tabla.column("#0", width=172, minwidth=120, anchor="w")
        for i in self.tabla["columns"]:
            self.tabla.column(i, width=172, minwidth=120, anchor="w")

        self.tabla.heading("#0", text="LEGAJO", anchor="w")
        for i in self.tabla["columns"]:
            self.tabla.heading(i, text=i, anchor="w")

        self.tabla.grid(row=0, column=0, sticky="ew")

        self.actualizar_treeview()

        if len(self.tabla.get_children()) == 0:
            self.boton_ver_datos.config(state="disabled")

        # FRAME FOOTER
        self.boton_cerrar = Button(self.frame_footer, text="Cerrar", command=lambda: self.cerrar())
        self.boton_cerrar.grid(row=0, column=0, padx=10, pady=10)

        self.frames = [self.frame_footer, self.frame_tabla, self.frame_input, self.frame_botones, self.root]
        self.botones = [self.boton_ver_datos, self.boton_modificar, self.boton_cerrar, self.boton_baja, self.boton_alta]
        self.labels = [self.label_area, self.resultado_pago_antiguedad, self.resultado_pago_presentismo,
                       self.resultado_vacaciones, self.resultado_antiguedad, self.label_vacaciones,
                       self.label_antiguedad, self.label_pago_antiguedad, self.label_pago_presentismo,
                       self.label_ingreso, self.label_legajo, self.label_sueldo, self.label_nombre, self.label_cuil,
                       self.label_apellido, self.menubar]

        self.auditor = observadores.AuditorRegistro()
        self.rrhh = observadores.DepartamentoRH()
        self.registrar = EmpleadoRegistro()
        self.registrar.registrar_observador(self.auditor)
        self.registrar.registrar_observador(self.rrhh)

    def no_cerrar_ventana(self):
        pass
    def tema_oscuro(self):
        """Cambia el aspecto del App tornandola mas oscura."""

        fondo = "gray20"
        foreground = "gray80"

        for frame in self.frames:
            frame.config(background=fondo)

        for label in self.labels:
            label.configure(background=fondo, foreground=foreground)

        for boton in self.botones:
            boton.config(background=fondo, fg=foreground)

    def tema_claro(self):
        """Cambia el aspecto del App tornandola mas oscura."""

        fondo = "#d3d3d3"
        foreground = "black"

        for frame in self.frames:
            frame.config(background=fondo)

        for label in self.labels:
            label.configure(background=fondo, foreground=foreground)

        for boton in self.botones:
            boton.config(background=fondo, fg=foreground)

    @registrar_info
    def alta(self):
        """
        LLama ala funcion alta en modelo.py y muestra la carga en el treeview.
        """
        try:
            patron = "^\d+$"
            if re.match(patron, self.cuil.get()):
                nuevo_empleado = EmpleadoORM(nombre=self.var_nombre.get(),
                                             apellido=self.var_apellido.get(),
                                             cuil=self.var_cuil.get(),
                                             area=self.var_area.get(),
                                             sueldo=self.var_sueldo.get(),
                                             fecha_ingreso=str(self.ingreso.get_date())
                                             )
                nuevo_empleado.save()
                self.limpiar()
                self.actualizar_treeview()
                messagebox.showinfo(title="Alta", message="Se cargo correctamente")
                self.registrar.agregar_empleado(nuevo_empleado.nombre_completo)
                return f"Se ingreso a {nuevo_empleado.nombre_completo()}"
            else:
                messagebox.showerror(
                    title="Error en el cuil",
                    message="El valor ingresado tiene que ser numérico, sin guiones ni espacios",
                )
                return f"ERROR AL INGRESAR EL CUIT DE {self.var_nombre.get()} {self.var_apellido.get()}"

        except IntegrityError:
            messagebox.showerror(title="Alta", message="El CUIL no se puede repetir")

    @registrar_info
    def baja(self):
        """LLama a la funcion baja de modelo.py y elimina el registro del treeview."""
        continuar = messagebox.askyesno(
            "Baja de empleado", "¿Esta seguro de borrar el empleado?"
        )
        if continuar:
            item = self.tabla.focus()
            legajo = self.tabla.item(item)["text"]
            empleado_orm = EmpleadoORM.get(EmpleadoORM.id == legajo)
            empleado_orm.delete_instance()
            self.tabla.delete(item)
            if len(self.tabla.get_children()) == 0:
                self.boton_ver_datos.config(state="disabled")
            self.entry_legajo.focus_set()

            return f"Se elimino a {empleado_orm.nombre_completo()}"
        else:
            pass

    def ver_datos(self):
        """Muestra en los entry los datos del empleado seleccionado previamente en el treeview."""
        item = self.tabla.focus()
        legajo = self.tabla.item(item)["text"]
        valores = self.tabla.item(item)["values"]
        self.var_legajo.set(legajo)
        self.var_nombre.set(valores[0])
        self.var_apellido.set(valores[1])
        self.var_area.set(valores[2])
        self.var_sueldo.set(valores[3])
        self.var_cuil.set(valores[4])
        fecha = datetime.date(int(valores[5].split("-")[0]), int(valores[5].split("-")[1]),
                              int(valores[5].split("-")[2]))
        self.ingreso.set_date(fecha)

        empleado = EmpleadoORM.get(EmpleadoORM.id == legajo)

        self.resultado_antiguedad.configure(text=f"{str(int(empleado.calcula_antiguedad() / 365.2425))} años")
        self.resultado_vacaciones.configure(text=str(empleado.calcula_vacaciones()))
        self.resultado_pago_antiguedad.configure(text=str(empleado.calcula_pago_antiguedad()))
        self.resultado_pago_presentismo.configure(text=str(empleado.calcula_pago_presentismo()))
        self.boton_modificar.config(state="normal")
        self.boton_ver_datos.config(state="disabled")
        self.boton_alta.config(state="disabled")
        self.boton_baja.config(state="disabled")
        self.entry_nombre.focus_set()
        self.boton_modificar.config(state="normal")
        self.boton_ver_datos.config(state="disabled")
        self.boton_alta.config(state="disabled")
        self.boton_baja.config(state="disabled")
        self.entry_nombre.focus_set()

    def limpiar(self):
        """
        Pone en blanco los Entry despues de un a accion y defa el foco en Nombre para continuar la carga de empleados.
        """
        self.var_legajo.set("")
        self.var_nombre.set("")
        self.var_apellido.set("")
        self.var_area.set("")
        self.var_sueldo.set("")
        self.var_cuil.set("")
        self.ingreso.set_date(datetime.datetime.today())
        self.boton_ver_datos.config(state="normal")
        self.boton_modificar.config(state="disabled")
        self.boton_alta.config(state="normal")
        self.boton_baja.config(state="normal")
        self.entry_nombre.focus_set()
        self.actualizar_treeview()

    @registrar_info
    def modificar(self):
        """
        LLama a la funcion modificar de modulo.py y muestra en pantalla el resultado de la accion a través de messagebox.
        """
        continuar = messagebox.askyesno(
            "Modificar empleado", "¿Esta seguro de modificar el empleado?"
        )
        if continuar:
            patron = "^\d+$"
            if re.match(patron, self.cuil.get()):
                empleado = EmpleadoORM.get(EmpleadoORM.id == self.var_legajo.get())
                nuevos_datos = {
                    "nombre": self.var_nombre.get(),
                    "apellido": self.var_apellido.get(),
                    "cuil": self.var_cuil.get(),
                    "area": self.var_area.get(),
                    "sueldo": self.var_sueldo.get(),
                    "fecha_ingreso": self.ingreso.get_date()
                }
                campos_modificados = {}

                for campo, valor_nuevo in nuevos_datos.items():
                    valor_actual = getattr(empleado, campo)
                    if valor_actual != valor_nuevo:
                        campos_modificados[campo] = {"De:": valor_actual, "A:": valor_nuevo}
                        setattr(empleado, campo, valor_nuevo)

                empleado.save()

                item = self.tabla.focus()
                self.tabla.item(
                    item,
                    text=self.var_legajo.get(),
                    values=(
                        self.var_nombre.get(),
                        self.var_apellido.get(),
                        self.var_area.get(),
                        self.var_sueldo.get(),
                        self.var_cuil.get(),
                        self.ingreso.get_date(),
                    ),
                )
                self.limpiar()
                self.registrar.actualizar_empleado(empleado, campos_modificados)
                info = ""
                for k, v in campos_modificados.items():
                    info += f" {k.upper()}:"
                    for kv, vv in v.items():
                        info += f" {kv}"
                        info += f" {vv}"
                return f"Se modifico {info}"
            else:
                messagebox.showerror(
                    title="Error en el cuil", message="Ingreselo sin guiones"
                )
                return f"ERROR AL MODIFICAR EL CUIT DE {self.var_nombre.get()} {self.var_apellido.get()}"
        else:
            self.limpiar()

    def actualizar_treeview(self):
        """
        Trae los datos de la base y actualiza el treeview.
        """
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)

        resultados_orm = EmpleadoORM().select()
        for empleado in resultados_orm:
            self.tabla.insert("", 0, text=empleado.id, values=(
                empleado.nombre, empleado.apellido, empleado.area, empleado.sueldo, empleado.cuil,
                empleado.fecha_ingreso))

    def cerrar(self):
        self.servidor.stop_server()
        self.root.quit()

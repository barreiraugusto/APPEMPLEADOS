from tkinter import *
from tkinter import ttk
import sqlite3
import re


# FUNCIONES PARA LA BASE DE DATOS


def conexion():
    con = sqlite3.connect("empleados.db")
    return con


def crear_tabla():
    con = conexion()
    try:
        cursor = con.cursor()
        sql = """CREATE TABLE empleado
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                legajo INTEGER UNIQUE,
                nombre varchar(20) NOT NULL,
                apellido varchar(20) NOT NULL,
                area varchar(20) NOT NULL,
                sueldo real NOT NULL,
                cuil varchar(10) NOT NULL,
                fecha_ingreso varchar(10) NOT NULL)
        """
        cursor.execute(sql)
        con.commit()
    except:
        pass


conexion()
crear_tabla()


def verificar_dato(legajo):
    patron = "^[\d]*$"  # regex para el campo cadena
    if re.match(patron, legajo):
        alta()
        alta_base()


def alta_base(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso):
    con = conexion()
    cursor = con.cursor()
    data = (legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso)
    sql = "INSERT INTO empleado(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso) VALUES(?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(sql, data)
    con.commit()


def baja_base(legajo):
    con = conexion()
    cursor = con.cursor()
    data = (legajo,)
    sql = "DELETE FROM empleado WHERE legajo = ?;"
    cursor.execute(sql, data)
    con.commit()


def modificar_base(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso):
    con = conexion()
    cursor = con.cursor()
    data = (nombre, apellido, area, sueldo, cuil, fecha_ingreso, legajo)
    sql = "UPDATE empleado SET nombre = ?, apellido = ?, area = ?, sueldo = ?, cuil = ?, fecha_ingreso = ? WHERE legajo = ?"
    cursor.execute(sql, data)
    con.commit()


######################## VISTA ########################

root = Tk()
root.title("ALTA Y BAJA DE PERSONAL")
root.resizable(0, 0)
p1 = PhotoImage(
    file="/home/augusto/Documentos/Diplomatura en Python/ENTREGA INTERMEDIA/CODIGO/APPEMPLEADOS/icono.png"
)
root.iconphoto(False, p1)

# FUNCIONES
def alta():
    alta_base(
        var_legajo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_area.get(),
        var_sueldo.get(),
        var_cuil.get(),
        var_ingreso.get(),
    )
    tabla.insert(
        "",
        "end",
        text=var_legajo.get(),
        values=(
            var_nombre.get(),
            var_apellido.get(),
            var_area.get(),
            var_sueldo.get(),
            var_cuil.get(),
            var_ingreso.get(),
        ),
    )

    legajo.delete(0, END)
    nombre.delete(0, END)
    apellido.delete(0, END)
    area.delete(0, END)
    sueldo.delete(0, END)
    cuil.delete(0, END)
    ingreso.delete(0, END)
    boton_ver_datos.config(state=NORMAL)


def baja():
    item = tabla.focus()
    legajo = tabla.item(item)["text"]
    baja_base(legajo)
    tabla.delete(item)
    if len(tabla.get_children()) == 0:
        boton_ver_datos.config(state="disabled")


def ver_datos():
    item = tabla.focus()
    texto = tabla.item(item)["text"]
    valores = tabla.item(item)["values"]
    legajo.insert(0, texto)
    nombre.insert(0, valores[0])
    apellido.insert(0, valores[1])
    area.insert(0, valores[2])
    sueldo.insert(0, valores[3])
    cuil.insert(0, valores[4])
    ingreso.insert(0, valores[5])
    boton_modificar.config(state="normal")
    boton_ver_datos.config(state=DISABLED)
    boton_alta.config(state=DISABLED)
    boton_baja.config(state=DISABLED)


def modificar():
    item = tabla.focus()
    tabla.item(
        item,
        text=var_legajo.get(),
        values=(
            var_nombre.get(),
            var_apellido.get(),
            var_area.get(),
            var_sueldo.get(),
            var_cuil.get(),
            var_ingreso.get(),
        ),
    )
    modificar_base(
        var_legajo.get(),
        var_nombre.get(),
        var_apellido.get(),
        var_area.get(),
        var_sueldo.get(),
        var_cuil.get(),
        var_ingreso.get(),
    )
    legajo.delete(0, END)
    nombre.delete(0, END)
    apellido.delete(0, END)
    area.delete(0, END)
    sueldo.delete(0, END)
    cuil.delete(0, END)
    ingreso.delete(0, END)
    boton_ver_datos.config(state="normal")
    boton_modificar.config(state=DISABLED)
    boton_alta.config(state="normal")
    boton_baja.config(state="normal")


def tema_oscuro():
    root.config(background="gray20")
    frame_botones.configure(background="gray20")
    frame_inputs.config(background="gray20")
    frame_tabla.config(background="gray20")
    frame_footer.config(background="gray20")
    label_apellido.configure(background="gray20", foreground="gray80")
    label_cuil.config(background="gray20", foreground="gray80")
    label_ingreso.config(background="gray20", foreground="gray80")
    label_nombre.config(background="gray20", foreground="gray80")
    label_sueldo.config(background="gray20", foreground="gray80")
    label_legajo.config(background="gray20", foreground="gray80")
    label_ingreso.config(background="gray20", foreground="gray80")
    label_area.config(background="gray20", foreground="gray80")
    boton_alta.config(background="gray20", fg="gray80")
    boton_baja.config(background="gray20", fg="gray80")
    boton_cerrar.config(background="gray20", fg="gray80")
    boton_modificar.config(background="gray20", fg="gray80")
    boton_ver_datos.config(background="gray20", fg="gray80")
    menubar.config(background="gray20", fg="gray80")


def tema_claro():
    root.config(background="#d3d3d3")
    frame_botones.configure(background="#d3d3d3")
    frame_inputs.config(background="#d3d3d3")
    frame_tabla.config(background="#d3d3d3")
    frame_footer.config(background="#d3d3d3")
    label_apellido.configure(background="#d3d3d3", foreground="black")
    label_cuil.config(background="#d3d3d3", foreground="black")
    label_ingreso.config(background="#d3d3d3", foreground="black")
    label_nombre.config(background="#d3d3d3", foreground="black")
    label_sueldo.config(background="#d3d3d3", foreground="black")
    label_legajo.config(background="#d3d3d3", foreground="black")
    label_ingreso.config(background="#d3d3d3", foreground="black")
    label_area.config(background="#d3d3d3", foreground="black")
    boton_alta.config(background="#d3d3d3", fg="black")
    boton_baja.config(background="#d3d3d3", fg="black")
    boton_cerrar.config(background="#d3d3d3", fg="black")
    boton_modificar.config(background="#d3d3d3", fg="black")
    boton_ver_datos.config(background="#d3d3d3", fg="black")
    menubar.config(background="#d3d3d3", fg="black")


def actualizar_treeview(tabla):
    records = tabla.get_children()
    for element in records:
        tabla.delete(element)

    sql = "SELECT * FROM empleado ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        tabla.insert(
            "",
            0,
            text=fila[1],
            values=(fila[2], fila[3], fila[4], fila[5], fila[6], fila[7]),
        )


# DECLARACION DE VARIABLES
var_legajo = StringVar()
var_nombre = StringVar()
var_apellido = StringVar()
var_cuil = StringVar()
var_area = StringVar()
var_sueldo = StringVar()
var_ingreso = StringVar()


frame_inputs = Frame(root)
frame_inputs.grid(row=0, column=0, pady=10, sticky=EW)

frame_botones = Frame(root)
frame_botones.grid(row=1, column=0, pady=10, sticky=E)

frame_tabla = Frame(root)
frame_tabla.grid(row=2, column=0, pady=10, sticky=EW)

frame_footer = Frame(root)
frame_footer.grid(row=3, column=0, pady=10, sticky=E)


# MENU
menubar = Menu(root)
root.config(menu=menubar)
menubar.configure(background="red")
apariencia = Menu(menubar, tearoff=0)
apariencia.add_command(label="Oscuro", command=lambda: tema_oscuro())
apariencia.add_command(label="Claro", command=lambda: tema_claro())

menubar.add_cascade(label="Apariencia", menu=apariencia)


# FRAME INPUTS
label_legajo = ttk.Label(frame_inputs, text=("N° de legajo"))
label_legajo.grid(row=0, column=0, padx=10, pady=10, sticky=W)
legajo = ttk.Entry(frame_inputs, textvariable=var_legajo, width=30)
legajo.grid(row=0, column=1, padx=10, pady=10, sticky=W)

label_nombre = ttk.Label(frame_inputs, text=("Nombre"))
label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky=W)
nombre = ttk.Entry(frame_inputs, textvariable=var_nombre, width=30)
nombre.grid(row=1, column=1, padx=10, pady=10, sticky=W)

label_apellido = ttk.Label(frame_inputs, text=("Apellido"))
label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky=W)
apellido = ttk.Entry(frame_inputs, textvariable=var_apellido, width=30)
apellido.grid(row=2, column=1, padx=10, pady=10, sticky=W)

label_cuil = ttk.Label(frame_inputs, text=("C.U.I.L."))
label_cuil.grid(row=3, column=0, padx=10, pady=10, sticky=W)
cuil = ttk.Entry(frame_inputs, textvariable=var_cuil, width=30)
cuil.grid(row=3, column=1, padx=10, pady=10, sticky=W)

label_area = ttk.Label(frame_inputs, text=("Area"))
label_area.grid(row=0, column=2, padx=10, pady=10, sticky=W)
area = ttk.Entry(frame_inputs, textvariable=var_area, width=30)
area.grid(row=0, column=3, padx=10, pady=10, sticky=W)

label_sueldo = ttk.Label(frame_inputs, text=("Sueldo"))
label_sueldo.grid(row=1, column=2, padx=10, pady=10, sticky=W)
sueldo = ttk.Entry(frame_inputs, textvariable=var_sueldo, width=30)
sueldo.grid(row=1, column=3, padx=10, pady=10, sticky=W)

label_ingreso = ttk.Label(frame_inputs, text=("Ingreso"))
label_ingreso.grid(row=2, column=2, padx=10, pady=10, sticky=W)
ingreso = ttk.Entry(frame_inputs, textvariable=var_ingreso, width=30)
ingreso.grid(row=2, column=3, padx=10, pady=10, sticky=W)

# FRAME BOTONES

boton_alta = Button(
    frame_botones, text="Alta", command=lambda: verificar_dato(var_legajo.get())
)
boton_alta.grid(row=0, column=0, padx=10, pady=10)
boton_baja = Button(frame_botones, text="Baja", command=lambda: baja())
boton_baja.grid(row=0, column=1, padx=10, pady=10)
boton_modificar = Button(
    frame_botones, text="Modificar", state=DISABLED, command=lambda: modificar()
)
boton_modificar.grid(row=0, column=2, padx=10, pady=10)

boton_ver_datos = Button(frame_botones, text="Ver datos", command=lambda: ver_datos())
boton_ver_datos.grid(row=0, column=3, padx=10, pady=10)


# FRAME TABLA

tabla = ttk.Treeview(frame_tabla)
tabla["columns"] = (
    "NOMBRE",
    "APELLIDO",
    "AREA",
    "SUELDO",
    "C.U.I.L.",
    "FECHA DE INGRESO",
)
tabla.column("#0", width=120, minwidth=120)
tabla.column("NOMBRE", width=120, minwidth=120)
tabla.column("APELLIDO", width=120, minwidth=120)
tabla.column("AREA", width=120, minwidth=120)
tabla.column("SUELDO", width=120, minwidth=120)
tabla.column("C.U.I.L.", width=120, minwidth=120)
tabla.column("FECHA DE INGRESO", width=120, minwidth=120)

tabla.heading("#0", text="Legajo")
tabla.heading("NOMBRE", text="Nombre")
tabla.heading("APELLIDO", text="Apellido")
tabla.heading("AREA", text="Area")
tabla.heading("SUELDO", text="Sueldo")
tabla.heading("C.U.I.L.", text="Cuil")
tabla.heading("FECHA DE INGRESO", text="Ingreso")
tabla.grid(row=0, column=0, padx=10, pady=10, sticky=EW)

actualizar_treeview(tabla)

if len(tabla.get_children()) == 0:
    boton_ver_datos.config(state="disabled")

# FRAME FOOTER

boton_cerrar = Button(frame_footer, text="Cerrar", command=root.quit)
boton_cerrar.grid(row=0, column=0, padx=10, pady=10)


root.mainloop()

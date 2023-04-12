import os
import re
from tkinter import messagebox, Button, Frame, StringVar, PhotoImage, Menu
from tkinter import ttk

from modelo import alta_base, baja_base, modificar_base, conexion


def tema_oscuro(root, frame_botones, frame_inputs, frame_tabla, frame_footer, label_apellido, label_cuil,
                label_nombre, label_sueldo, label_legajo, label_ingreso, label_area, boton_alta,
                boton_baja, boton_cerrar, boton_modificar, boton_ver_datos, menubar):
    root.config(background="gray20")
    frame_botones.configure(background="gray20")
    frame_inputs.config(background="gray20")
    frame_tabla.config(background="gray20")
    frame_footer.config(background="gray20")
    label_apellido.configure(background="gray20", foreground="gray80")
    label_cuil.config(background="gray20", foreground="gray80")
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


def tema_claro(root, frame_botones, frame_inputs, frame_tabla, frame_footer, label_apellido, label_cuil,
               label_nombre, label_sueldo, label_legajo, label_ingreso, label_area, boton_alta,
               boton_baja, boton_cerrar, boton_modificar, boton_ver_datos, menubar):
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


# FUNCIONES
def alta(var_tabla, legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, entry_legajo):
    try:
        patron = "^\d+$"
        if re.match(patron, cuil.get()):
            alta_base(
                nombre.get(),
                apellido.get(),
                area.get(),
                sueldo.get(),
                cuil.get(),
                fecha_ingreso.get(),
            )
            var_tabla.insert(
                "",
                "end",
                text=legajo.get(),
                values=(
                    nombre.get(),
                    apellido.get(),
                    area.get(),
                    sueldo.get(),
                    cuil.get(),
                    fecha_ingreso.get(),
                ),
            )
            nombre.set("")
            apellido.set("")
            area.set("")
            sueldo.set("")
            cuil.set("")
            fecha_ingreso.set("")
            boton_ver_datos.config(state="normal")
            messagebox.showinfo(title="Alta", message="Se cargo correctamente")
            entry_legajo.focus_set()
            actualizar_treeview(var_tabla)
        else:
            messagebox.showerror(
                title="Error en el cuil",
                message="El valor ingresado tiene que ser numérico, sin guiones ni spacios",
            )
    except:
        messagebox.showerror(title="Alta", message="Error al cargar")


def baja(tabla, entry_legajo, boton_ver_datos):
    continuar = messagebox.askyesno(
        "Baja de empleado", "¿Esta seguro de borrar el empleado?"
    )
    if continuar:
        item = tabla.focus()
        legajo = tabla.item(item)["text"]
        baja_base(legajo)
        tabla.delete(item)
        if len(tabla.get_children()) == 0:
            boton_ver_datos.config(state="disabled")
        entry_legajo.focus_set()
    else:
        pass


def ver_datos(tabla, legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, boton_modificar,
              boton_alta, boton_baja, entry_nombre):
    item = tabla.focus()
    texto = tabla.item(item)["text"]
    valores = tabla.item(item)["values"]
    legajo.set(texto)
    nombre.set(valores[0])
    apellido.set(valores[1])
    area.set(valores[2])
    sueldo.set(valores[3])
    cuil.set(valores[4])
    fecha_ingreso.set(valores[5])
    boton_modificar.config(state="normal")
    boton_ver_datos.config(state="disabled")
    boton_alta.config(state="disabled")
    boton_baja.config(state="disabled")
    entry_nombre.focus_set()


def limpiar(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, boton_modificar, boton_alta,
            boton_baja, entry_nombre):
    legajo.set("")
    nombre.set("")
    apellido.set("")
    area.set("")
    sueldo.set("")
    cuil.set("")
    fecha_ingreso.set("")
    boton_ver_datos.config(state="normal")
    boton_modificar.config(state="disabled")
    boton_alta.config(state="normal")
    boton_baja.config(state="normal")
    entry_nombre.focus_set()


def modificar(tabla, legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, boton_modificar,
              boton_alta, boton_baja, entry_nombre):
    continuar = messagebox.askyesno(
        "Modificar empleado", "¿Esta seguro de modificar el empleado?"
    )
    if continuar:
        patron = "^\d+$"
        if re.match(patron, cuil.get()):
            modificar_base(
                legajo.get(),
                nombre.get(),
                apellido.get(),
                area.get(),
                sueldo.get(),
                cuil.get(),
                fecha_ingreso.get(),
            )
            item = tabla.focus()
            tabla.item(
                item,
                text=legajo.get(),
                values=(
                    nombre.get(),
                    apellido.get(),
                    area.get(),
                    sueldo.get(),
                    cuil.get(),
                    fecha_ingreso.get(),
                ),
            )
            # LIMPIAMOS LOS ENTRY
            limpiar(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, boton_modificar,
                    boton_alta, boton_baja, entry_nombre)
        else:
            messagebox.showerror(
                title="Error en el cuil", message="Ingreselo sin guiones"
            )
    else:
        limpiar(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso, boton_ver_datos, boton_modificar,
                boton_alta, boton_baja, entry_nombre)


def actualizar_treeview(tabla):
    records = tabla.get_children()
    for element in records:
        tabla.delete(element)

    sql = "SELECT * FROM empleado ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)
    resultado = datos.fetchall()
    resultado.sort()
    for fila in resultado:
        tabla.insert(
            "",
            0,
            text=fila[0],
            values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]),
        )


def principal(root):
    root.title("ALTA Y BAJA DE PERSONAL")
    root.resizable(False, False)

    try:
        ruta_icono = os.path.join(os.path.dirname(__file__), "img/icono.png")
        root.iconphoto(False, PhotoImage(file=ruta_icono))
    except:
        pass

    # DECLARACION DE VARIABLES DE TKINTER
    var_legajo = StringVar()
    var_nombre = StringVar()
    var_apellido = StringVar()
    var_cuil = StringVar()
    var_area = StringVar()
    var_sueldo = StringVar()
    var_ingreso = StringVar()

    # DECLARACION DE LOS FRAMES QUE SECTORIZAN EL ROOT
    frame_inputs = Frame(root)
    frame_inputs.grid(row=0, column=0, pady=10, sticky="ew")

    frame_botones = Frame(root)
    frame_botones.grid(row=1, column=0, pady=10, sticky="e")

    frame_tabla = Frame(root)
    frame_tabla.grid(row=2, column=0, sticky="ew")

    frame_footer = Frame(root)
    frame_footer.grid(row=3, column=0, pady=10, sticky="e")

    # MENU
    menubar = Menu(root)
    root.config(menu=menubar)
    apariencia = Menu(menubar, tearoff=0)
    apariencia.add_command(label="Oscuro",
                           command=lambda: tema_oscuro(root, frame_botones, frame_inputs, frame_tabla, frame_footer,
                                                       label_apellido, label_cuil,
                                                       label_nombre, label_sueldo, label_legajo, label_ingreso,
                                                       label_area, boton_alta,
                                                       boton_baja, boton_cerrar, boton_modificar, boton_ver_datos,
                                                       menubar))
    apariencia.add_command(label="Claro",
                           command=lambda: tema_claro(root, frame_botones, frame_inputs, frame_tabla, frame_footer,
                                                      label_apellido, label_cuil,
                                                      label_nombre, label_sueldo, label_legajo, label_ingreso,
                                                      label_area, boton_alta,
                                                      boton_baja, boton_cerrar, boton_modificar, boton_ver_datos,
                                                      menubar))
    menubar.add_cascade(label="Apariencia", menu=apariencia)

    # FRAME INPUTS
    label_legajo = ttk.Label(frame_inputs, text="N° de legajo")
    label_legajo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    entry_legajo = ttk.Entry(
        frame_inputs, textvariable=var_legajo, width=30, state="readonly"
    )
    entry_legajo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    label_nombre = ttk.Label(frame_inputs, text="Nombre")
    label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_nombre = ttk.Entry(frame_inputs, textvariable=var_nombre, width=30)
    entry_nombre.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    label_apellido = ttk.Label(frame_inputs, text="Apellido")
    label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    apellido = ttk.Entry(frame_inputs, textvariable=var_apellido, width=30)
    apellido.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    label_cuil = ttk.Label(frame_inputs, text="C.U.I.L.")
    label_cuil.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    cuil = ttk.Entry(frame_inputs, textvariable=var_cuil, width=30)
    cuil.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    label_area = ttk.Label(frame_inputs, text="Area")
    label_area.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    area = ttk.Entry(frame_inputs, textvariable=var_area, width=30)
    area.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    label_sueldo = ttk.Label(frame_inputs, text="Sueldo")
    label_sueldo.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    sueldo = ttk.Entry(frame_inputs, textvariable=var_sueldo, width=30)
    sueldo.grid(row=1, column=3, padx=10, pady=10, sticky="w")

    label_ingreso = ttk.Label(frame_inputs, text="Ingreso")
    label_ingreso.grid(row=2, column=2, padx=10, pady=10, sticky="w")
    ingreso = ttk.Entry(frame_inputs, textvariable=var_ingreso, width=30)
    ingreso.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    # FRAME BOTONES

    boton_alta = Button(
        frame_botones,
        text="Alta",
        command=lambda: alta(
            tabla,
            var_legajo,
            var_nombre,
            var_apellido,
            var_area,
            var_sueldo,
            var_cuil,
            var_ingreso,
            boton_ver_datos,
            entry_legajo,
        ),
    )
    boton_alta.grid(row=0, column=0, padx=10, pady=10)

    boton_baja = Button(frame_botones, text="Baja", command=lambda: baja(tabla, entry_legajo, boton_ver_datos))
    boton_baja.grid(row=0, column=1, padx=10, pady=10)

    boton_modificar = Button(
        frame_botones,
        text="Modificar",
        state="disabled",
        command=lambda: modificar(
            tabla,
            var_legajo,
            var_nombre,
            var_apellido,
            var_area,
            var_sueldo,
            var_cuil,
            var_ingreso,
            boton_ver_datos,
            boton_modificar,
            boton_alta,
            boton_baja,
            entry_nombre
        ),
    )
    boton_modificar.grid(row=0, column=2, padx=10, pady=10)

    boton_ver_datos = Button(
        frame_botones,
        text="Ver datos",
        command=lambda: ver_datos(
            tabla,
            var_legajo,
            var_nombre,
            var_apellido,
            var_area,
            var_sueldo,
            var_cuil,
            var_ingreso,
            boton_ver_datos,
            boton_modificar,
            boton_alta,
            boton_baja,
            entry_nombre,
        ),
    )
    boton_ver_datos.grid(row=0, column=3, padx=10, pady=10)

    # FRAME TABLA

    tabla = ttk.Treeview(frame_tabla)
    tabla["columns"] = (
        "NOMBRE",
        "APELLIDO",
        "AREA",
        "SUELDO",
        "C.U.I.L.",
        "INGRESO",
    )
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tabla.configure(yscrollcommand=scrollbar.set)

    tabla.column("#0", width=120, minwidth=120, anchor="w")
    for i in tabla["columns"]:
        tabla.column(i, width=120, minwidth=120, anchor="w")

    tabla.heading("#0", text="LEGAJO", anchor="w")
    for i in tabla["columns"]:
        tabla.heading(i, text=i, anchor="w")

    tabla.grid(row=0, column=0, sticky="ew")

    actualizar_treeview(tabla)

    if len(tabla.get_children()) == 0:
        boton_ver_datos.config(state="disabled")

    # FRAME FOOTER
    boton_cerrar = Button(frame_footer, text="Cerrar", command=root.quit)
    boton_cerrar.grid(row=0, column=0, padx=10, pady=10)

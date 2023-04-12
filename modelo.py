import sqlite3


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


def alta_base(nombre, apellido, area, sueldo, cuil, fecha_ingreso):
    con = conexion()
    cursor = con.cursor()
    data = (nombre, apellido, area, sueldo, cuil, fecha_ingreso)
    sql = "INSERT INTO empleado(nombre, apellido, area, sueldo, cuil, fecha_ingreso) VALUES(?, ?, ?, ?, ?, ?);"
    cursor.execute(sql, data)
    con.commit()


def baja_base(legajo):
    con = conexion()
    cursor = con.cursor()
    id = legajo
    data = (id,)
    sql = "DELETE FROM empleado WHERE id = ?;"
    cursor.execute(sql, data)
    con.commit()


def modificar_base(legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso):
    con = conexion()
    cursor = con.cursor()
    id = legajo
    data = (nombre, apellido, area, sueldo, cuil, fecha_ingreso, id)
    sql = "UPDATE empleado SET nombre = ?, apellido = ?, area = ?, sueldo = ?, cuil = ?, fecha_ingreso = ? WHERE id = ?"
    cursor.execute(sql, data)
    con.commit()



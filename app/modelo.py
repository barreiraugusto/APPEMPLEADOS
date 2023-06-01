"""
Este módulo contiene funciones para interactuar con una base de datos SQLite que contiene información de empleados.
"""
import sqlite3


class Modelo:
    def __init__(self):
        self.conexion = self.conexion()
        self.cursor = self.conexion.cursor()

    def conexion(self):
        """
        Establece una conexión con la base de datos ubicada en la ruta "../empleados.db" y la devuelve.
    
        :return: Devuelve la conexion.
        """
        con = sqlite3.connect("../empleados.db")
        self.crear_tabla()
        return con

    def crear_tabla(self):
        """
        Crea una tabla llamada "empleado" en la base de datos, que tiene las columnas "id", "nombre", "apellido", "area",
        "sueldo", "cuil" y "fecha_ingreso".
    
        """
        try:
            sql = """CREATE TABLE empleado
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre varchar(20) NOT NULL,
                    apellido varchar(20) NOT NULL,
                    area varchar(20) NOT NULL,
                    sueldo real NOT NULL,
                    cuil varchar(10) NOT NULL,
                    fecha_ingreso varchar(10) NOT NULL)
            """
            self.cursor.execute(sql)
            self.conexion.commit()
        except:
            pass

    #   try:
    #        conexion()
    #        crear_tabla()
    #    except:
    #        pass

    def alta_base(self, nombre, apellido, area, sueldo, cuil, fecha_ingreso):
        """
        Agrega un nuevo registro a la tabla "empleado" con los datos del empleado proporcionados.
    
        :param nombre: Nombre del empleado.
        :param apellido: Apellido del empleado.
        :param area: Area en el que desempeña su labor.
        :param sueldo: Remuneracion mensual.
        :param cuil: Clave unica de identificacion laboral.
        :param fecha_ingreso: Fecha de ingreso a la empresa.
        """

        data = (nombre, apellido, area, sueldo, cuil, fecha_ingreso)
        sql = "INSERT INTO empleado(nombre, apellido, area, sueldo, cuil, fecha_ingreso) VALUES(?, ?, ?, ?, ?, ?);"
        self.cursor.execute(sql, data)
        self.conexion.commit()

    def baja_base(self, legajo):
        """
        Elimina de la tabla "empleado" el registro correspondiente al empleado identificado por el número de legajo proporcionado.
    
        :param legajo: Numero unico que identifica al empleado en la empresa.
        """
        id = legajo
        data = (id,)
        sql = "DELETE FROM empleado WHERE id = ?;"
        self.cursor.execute(sql, data)
        self.conexion.commit()

    def buscar(self, seleccion, valor):
        data = (valor,)
        sql = f'SELECT * FROM empleado WHERE {seleccion} = ?'
        cursor = self.conexion.cursor()
        datos = cursor.execute(sql, data)
        resultado = datos.fetchall()
        return resultado

    def consultar_base(self):
        """
        Consulta a la base de datos en base al parametro elemento.

        :return: El resultado de la consulta como una lista
        """
        sql = "SELECT * FROM empleado ORDER BY id ASC"
        cursor = self.conexion.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        resultado.sort()
        return resultado

    def modificar_base(self, legajo, nombre, apellido, area, sueldo, cuil, fecha_ingreso):
        """
        Actualiza los datos del registro correspondiente al empleado identificado por el número de legajo proporcionado
        en la tabla "empleado" con los nuevos valores de los datos proporcionados.

        :param legajo: Numero unico que identifica al empleado en la empresa.
        :param nombre: Nombre del empleado.
        :param apellido: Apellido del empleado.
        :param area: Area en el que desempeña su labor.
        :param sueldo: Remuneracion mensual.
        :param cuil: Clave unica de identificacion laboral.
        :param fecha_ingreso: Fecha de ingreso a la empresa.
        """
        id = legajo
        data = (nombre, apellido, area, sueldo, cuil, fecha_ingreso, id)
        sql = "UPDATE empleado SET nombre = ?, apellido = ?, area = ?, sueldo = ?, cuil = ?, fecha_ingreso = ? WHERE id = ?"
        self.cursor.execute(sql, data)
        self.conexion.commit()

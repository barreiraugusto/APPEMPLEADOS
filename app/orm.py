"""
Este módulo define un modelo de empleado utilizando Peewee como ORM y crea una base de datos SQLite llamada
"empleadosORM.db" con una tabla correspondiente al modelo de empleado. También incluye métodos para calcular la
antigüedad, los días de vacaciones y los pagos relacionados con el empleado.
"""
import datetime
import logging

from peewee import SqliteDatabase, Model, CharField

from app.decoradores import registrar_info

# Configuración básica del registro (log)
logging.basicConfig(filename='app.log', level=logging.INFO)

database = SqliteDatabase("empleadosORM.db")


class BaseModel(Model):
    class Meta:
        database = database


class EmpleadoORM(BaseModel):
    """
    Clase que representa un modelo de empleado y hereda de BaseModel.
    """
    nombre = CharField()
    apellido = CharField()
    cuil = CharField(unique=True)
    area = CharField()
    sueldo = CharField()
    fecha_ingreso = CharField()

    @registrar_info
    def calcula_antiguedad(self):
        """
        Calculo de la antiguedad del empleado calculado en base a la fecha de ingreso y la fecha actual al momento de
        consultar.

        :return: Devuelve la antiguedad en dias, la cual es usada para los diferentes calculos.
        """
        fecha_actual = datetime.date.today()
        fecha = datetime.date(int(str(self.fecha_ingreso).split("-")[0]), int(str(self.fecha_ingreso).split("-")[1]),
                              int(str(self.fecha_ingreso).split("-")[2]))
        fecha_ingreso_formateada = fecha
        antiguedad = fecha_actual - fecha_ingreso_formateada
        return antiguedad.days

    @registrar_info
    def calcula_vacaciones(self):
        """
        Calcula los dias de vacaciones que le corresponden segun la antiguedad calculada en el metodo
        calcula_antiguidad().

        :return: Devuelve un tipo string con los dias de vaciones que le corresponden al empleado.
        """
        antiguedad_en_dias = self.calcula_antiguedad()
        dias_vacaciones = ""
        if antiguedad_en_dias < 150:
            dias_vacaciones = f'{antiguedad_en_dias / 20} dias'
        if 150 < antiguedad_en_dias < 1826:
            dias_vacaciones = "2 semanas de franco a franco"
        if 1826 < antiguedad_en_dias < 3652:
            dias_vacaciones = "17 días hábiles o 21 corridos"
        if 3652 < antiguedad_en_dias < 10957:
            dias_vacaciones = "20 días hábiles o 28 corridos"
        if antiguedad_en_dias > 10957:
            dias_vacaciones = "30 días hábiles"
        return dias_vacaciones

    @registrar_info
    def calcula_pago_presentismo(self):
        """
        Calcula una suma fija o un porcentaje del sueldo básico que se otorga a los trabajadores que no faltaron
        en todo el mes.

        :return: Devuelve el monto en un dato del tipy float.
        """
        return round(float(self.sueldo) * 0.1)

    @registrar_info
    def calcula_pago_antiguedad(self):
        """
        Calcula el pago que debe recibir por su antiguedad calculada en el metodo calcula_antiguedad().

        :return: Devuelve un valor de tipo float con dos decimales equivalente al pago
        """
        year_trabajados = self.calcula_antiguedad() / 365.2425
        pago = float(self.sueldo) * 0.01 * year_trabajados
        return round(pago, 2)

    def nombre_completo(self):
        """
        Concatena el nombre y el apellido del enpleado.

        :return: Devuelve el nombre completo del empleado.
        """
        return f"{self.nombre} {self.apellido}"


database.connect()
database.create_tables([EmpleadoORM])


class EmpleadoRegistro:
    def __init__(self):
        self._empleados = []
        self._observadores = []

    def agregar_empleado(self, empleado):
        self._empleados.append(empleado)
        self.notificar_observadores("Se ha agregado un nuevo empleado.")

    def actualizar_empleado(self, empleado, nueva_informacion):
        print("actualizar empleado")
        self.notificar_observadores(f"Se ha actualizado la información de {empleado}\nInformacion:{nueva_informacion}")

    def registrar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        print(self._observadores)
        for observador in self._observadores:
            observador.actualizar(mensaje)

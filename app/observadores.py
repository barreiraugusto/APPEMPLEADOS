
class Observador:
    def actualizar(self, mensaje):
        pass


class AuditorRegistro(Observador):
    def actualizar(self, mensaje):
        print("Auditor: ", mensaje)


class DepartamentoRH(Observador):
    def actualizar(self, mensaje):
        print("Departamento de Recursos Humanos: ", mensaje)

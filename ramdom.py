from peewee import (
    Model, TextField, CharField, DateField, AutoField, SQL
)
from REPOSITORIO.conexion import conectar  # cambia "conexion" por el nombre del archivo donde está conectar()

base_datos = conectar()


class BaseModel(Model):
    class Meta:
        database = base_datos


class Proyecto(BaseModel):
    descripcion = TextField(null=True)
    fecha_creacion = DateField(constraints=[SQL("DEFAULT (curdate())")])
    id_proyecto = AutoField()
    nombre_proyecto = CharField(max_length=100)

    class Meta:
        table_name = "proyecto"


def listar_proyectos():
    return list(Proyecto.select())


if __name__ == "__main__":
    proyectos = listar_proyectos()
    for proyecto in proyectos:
        print(f'{proyecto.id_proyecto}-{proyecto.nombre_proyecto}-{proyecto.descripcion}-{proyecto.fecha_creacion}')
    

  
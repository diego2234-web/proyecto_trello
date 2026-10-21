import datetime
from peewee import (
    Model, AutoField, CharField, TextField, DateField, DateTimeField,
    IntegerField, ForeignKeyField, CompositeKey
)
from REPOSITORIO.conexion import conectar

db = conectar()


class BaseModel(Model):
    class Meta:
        database = db


class Proyecto(BaseModel):
    id_proyecto = AutoField()
    nombre_proyecto = CharField(max_length=100)
    descripcion = TextField(null=True)
    fecha_creacion = DateField(default=datetime.date.today)

    class Meta:
        table_name = 'PROYECTO'


class Usuario(BaseModel):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    email = CharField(max_length=150, unique=True)

    class Meta:
        table_name = 'USUARIO'


class ProyectoUsuario(BaseModel):
    proyecto = ForeignKeyField(Proyecto, column_name='id_proyecto', backref='miembros', on_delete='CASCADE')
    usuario = ForeignKeyField(Usuario, column_name='id_usuario', backref='proyectos', on_delete='CASCADE')
    rol = CharField(max_length=50)

    class Meta:
        table_name = 'PROYECTO_USUARIO'
        primary_key = CompositeKey('proyecto', 'usuario')


class Tablero(BaseModel):
    id_tablero = AutoField()
    proyecto = ForeignKeyField(Proyecto, column_name='id_proyecto', backref='tableros', on_delete='CASCADE')
    titulo = CharField(max_length=100)

    class Meta:
        table_name = 'TABLERO'


class Lista(BaseModel):
    id_lista = AutoField()
    tablero = ForeignKeyField(Tablero, column_name='id_tablero', backref='listas', on_delete='CASCADE')
    nombre_lista = CharField(max_length=100)
    posicion = IntegerField()

    class Meta:
        table_name = 'LISTA'


class Tarjeta(BaseModel):
    id_tarjeta = AutoField()
    lista = ForeignKeyField(Lista, column_name='id_lista', backref='tarjetas', on_delete='CASCADE')
    titulo = CharField(max_length=150)
    descripcion = TextField(null=True)
    fecha_limite = DateField(null=True)
    estado = CharField(max_length=50, null=True)

    class Meta:
        table_name = 'TARJETA'


class Comentario(BaseModel):
    id_comentario = AutoField()
    tarjeta = ForeignKeyField(Tarjeta, column_name='id_tarjeta', backref='comentarios', on_delete='CASCADE')
    usuario = ForeignKeyField(Usuario, column_name='id_usuario', backref='comentarios', on_delete='CASCADE')
    texto = TextField()
    fecha_creacion = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'COMENTARIO'


class Etiqueta(BaseModel):
    id_etiqueta = AutoField()
    nombre = CharField(max_length=50)
    color = CharField(max_length=20)

    class Meta:
        table_name = 'ETIQUETA'


class AsignacionTarjeta(BaseModel):
    tarjeta = ForeignKeyField(Tarjeta, column_name='id_tarjeta', backref='asignaciones', on_delete='CASCADE')
    usuario = ForeignKeyField(Usuario, column_name='id_usuario', backref='asignaciones', on_delete='CASCADE')

    class Meta:
        table_name = 'ASIGNACION_TARJETA'
        primary_key = CompositeKey('tarjeta', 'usuario')


class TarjetaEtiqueta(BaseModel):
    tarjeta = ForeignKeyField(Tarjeta, column_name='id_tarjeta', backref='etiquetas', on_delete='CASCADE')
    etiqueta = ForeignKeyField(Etiqueta, column_name='id_etiqueta', backref='tarjetas', on_delete='CASCADE')

    class Meta:
        table_name = 'TARJETA_ETIQUETA'
        primary_key = CompositeKey('tarjeta', 'etiqueta')
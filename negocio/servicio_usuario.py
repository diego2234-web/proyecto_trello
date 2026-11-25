from prettytable import PrettyTable
from REPOSITORIO.repositorio_usario import (
    listado_usuarios_habilitados,
    listado_usuarios_deshabilitados,
    guardar_usuario,
)
from REPOSITORIO.models import Usuario
from auxiliares import mensaje_error
GENEROS = {1: "Masculino", 2: "Femenino", 3: "Otro"}


def procesar_listado_usuario(habilitados: bool = True):
    """Muestra en tabla los usuarios habilitados (o deshabilitados)."""
    try:
        if habilitados:
            usuarios = listado_usuarios_habilitados()
        else:
            usuarios = listado_usuarios_deshabilitados()

        if not usuarios:
            print("No hay usuarios para mostrar.")
            return

        tabla = PrettyTable()
        tabla.field_names = ["ID", "RUT", "Nombre", "Apellido", "Correo", "Género"]
        for usuario in usuarios:
            tabla.add_row([
                usuario.id,
                usuario.rut,
                usuario.nombre,
                usuario.apellido,
                usuario.correo,
                GENEROS.get(usuario.genero, "Otro"),
            ])
        print(tabla)
    except Exception as error:
        mensaje_error(f"Ha ocurrido un error al listar: {error}")


def obtener_ticket_nombre(rut: str, nombre: str, apellido: str, correo: str, genero: int):
    """Crea un usuario con los datos recibidos y lo guarda."""
    try:
        usuario = Usuario(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            genero=genero,
            habilitado=True,
        )
        return guardar_usuario(usuario)
    except Exception as error:
        mensaje_error(f"Ha ocurrido un error al guardar: {error}")
        return None

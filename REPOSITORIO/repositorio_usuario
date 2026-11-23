# REPOSITORIO/repositorio_usario.py
from REPOSITORIO.conexion import base_datos
from REPOSITORIO.models import Usuario 
database = base_datos()


def listado_usuarios_habilitados():
    """Retorna todos los usuarios habilitados en la base de datos."""
    try:
        return list(Usuario.select().where(Usuario.habilitado == True))
    except Exception as error:
        print(f"Ha ocurrido un error al listar: {error}")
        return []


def listado_usuarios_deshabilitados():
    """Retorna todos los usuarios deshabilitados en la base de datos."""
    try:
        return list(Usuario.select().where(Usuario.habilitado == False))
    except Exception as error:
        print(f"Ha ocurrido un error al listar: {error}")
        return []


def obtener_usuario_por_id(id_usuario):
    """Retorna un usuario por su id o None si no existe."""
    try:
        return Usuario.get_or_none(Usuario.id == id_usuario)
    except Exception as error:
        print(f"Ha ocurrido un error al obtener el usuario: {error}")
        return None


def guardar_usuario(usuario_a_guardar):
    """Guarda (inserta o actualiza) un usuario y lo retorna."""
    try:
        usuario_a_guardar.save()
        return usuario_a_guardar
    except Exception as error:
        print(f"Ha ocurrido un error al guardar: {error}")
        return None

   
    

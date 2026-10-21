from REPOSITORIO.conexion import base_datos
from REPOSITORIO.models import Tarea  # O el modelo que corresponda a tu proyecto Trello

database = base_datos()

def listado_tareas():
    """Retorna todas las tareas registradas en la base de datos."""
    try:
        tareas = Tarea.select()
        return tareas
    except Exception as error:
        print(f"Ha ocurrido un error al listar: {error}")
        return []

def guardar_tarea(tarea_a_guardar):
    """Guarda un registro de tarea manejando excepciones de manera segura."""
    try:
        tarea_nueva = tarea_a_guardar.save()
        return tarea_nueva
    except Exception as error:
        print(f"Ha ocurrido un error al guardar: {error}")
        return None
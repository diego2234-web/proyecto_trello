from datetime import date
from auxiliares.config import nombre_app, version_app
from negocio.servicio_trello import ServicioTrello

servicio = ServicioTrello()


# ---------- Utilidades ----------
def mostrar_menu(titulo, opciones):
    print(f"\n{titulo}")
    print("=" * 40)
    for clave, valor in opciones.items():
        print(f"[{clave}] {valor}")
    print("=" * 40)


def pedir_int(mensaje):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("Debes ingresar un número.")
        return None


def pedir_texto(mensaje, obligatorio=True):
    texto = input(mensaje).strip()
    if obligatorio and not texto:
        print("Este campo no puede estar vacío.")
        return None
    return texto or None


def pedir_fecha(mensaje):
    texto = input(mensaje).strip()
    if not texto:
        return None
    try:
        return date.fromisoformat(texto)
    except ValueError:
        print("Formato inválido (AAAA-MM-DD). Se guardará sin fecha.")
        return None


def ejecutar_submenu(titulo, opciones, acciones):
    while True:
        mostrar_menu(titulo, opciones)
        opcion = input("Selecciona una opción: ").strip()
        if opcion == '0':
            break
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida, intenta de nuevo.")


# ---------- Mostrar listados ----------
def mostrar_tablas():
    tablas = servicio.listar_tablas()
    print("\nTablas en la base de datos:")
    if not tablas:
        print("  (no hay tablas)")
    for tabla in tablas:
        print(f"  - {tabla}")


def mostrar_proyectos():
    proyectos = servicio.listar_proyectos()
    print("\nProyectos:")
    if not proyectos:
        print("  (no hay proyectos)")
    for p in proyectos:
        print(f"  [{p.id_proyecto}] {p.nombre_proyecto} - {p.fecha_creacion}")
    return proyectos


def mostrar_tableros(id_proyecto=None):
    tableros = servicio.listar_tableros(id_proyecto)
    print("\nTableros:")
    if not tableros:
        print("  (no hay tableros)")
    for t in tableros:
        print(f"  [{t.id_tablero}] {t.titulo} (proyecto {t.proyecto_id})")
    return tableros


def mostrar_listas(id_tablero):
    listas = servicio.listar_listas(id_tablero)
    print("\nListas:")
    if not listas:
        print("  (no hay listas)")
    for l in listas:
        print(f"  [{l.id_lista}] {l.posicion}. {l.nombre_lista}")
    return listas


def mostrar_tarjetas(id_lista):
    tarjetas = servicio.listar_tarjetas(id_lista)
    print("\nTarjetas:")
    if not tarjetas:
        print("  (no hay tarjetas)")
    for t in tarjetas:
        limite = t.fecha_limite or "sin fecha"
        print(f"  [{t.id_tarjeta}] {t.titulo} | {t.estado} | límite: {limite}")
    return tarjetas


def mostrar_usuarios():
    usuarios = servicio.listar_usuarios()
    print("\nUsuarios:")
    if not usuarios:
        print("  (no hay usuarios)")
    for u in usuarios:
        print(f"  [{u.id_usuario}] {u.nombre} - {u.email}")
    return usuarios


def mostrar_etiquetas():
    etiquetas = servicio.listar_etiquetas()
    print("\nEtiquetas:")
    if not etiquetas:
        print("  (no hay etiquetas)")
    for e in etiquetas:
        print(f"  [{e.id_etiqueta}] {e.nombre} ({e.color})")
    return etiquetas


# ---------- Proyectos y tableros ----------
def crear_proyecto():
    nombre = pedir_texto("Nombre del proyecto: ")
    if not nombre:
        return
    descripcion = pedir_texto("Descripción (opcional): ", False)
    id_nuevo = servicio.crear_proyecto(nombre, descripcion)
    if id_nuevo:
        print(f"Proyecto creado con id {id_nuevo}.")


def crear_tablero():
    mostrar_proyectos()
    id_proyecto = pedir_int("Idproyecto: ")
    if id_proyecto is None:
        return
    titulo = pedir_texto("Título del tablero: ")
    if not titulo:
        return
    id_nuevo = servicio.crear_tablero(id_proyecto, titulo)
    if id_nuevo:
        print(f"Tablero creado con id {id_nuevo}.")


def listar_tableros():
    mostrar_proyectos()
    id_proyecto = pedir_int("Id del proyecto (Enter = todos): ")
    mostrar_tableros(id_proyecto)


def gestionar_proyectos():
    opciones = {
        '1': 'Crear proyecto',
        '2': 'Listar proyectos',
        '3': 'Crear tablero',
        '4': 'Listar tableros',
        '0': 'Volver'
    }
    acciones = {
        '1': crear_proyecto,
        '2': mostrar_proyectos,
        '3': crear_tablero,
        '4': listar_tableros
    }
    ejecutar_submenu("Gestión de Proyectos", opciones, acciones)


# ---------- Tareas (listas, tarjetas, comentarios, etiquetas) ----------
def elegir_tablero():
    if not mostrar_tableros():
        return None
    return pedir_int("Id del tablero: ")


def crear_lista():
    id_tablero = elegir_tablero()
    if id_tablero is None:
        return
    nombre = pedir_texto("Nombre de la lista (ej: Por hacer): ")
    if not nombre:
        return
    id_nuevo = servicio.crear_lista(id_tablero, nombre)
    if id_nuevo:
        print(f"Lista creada con id {id_nuevo}.")


def listar_listas():
    id_tablero = elegir_tablero()
    if id_tablero is not None:
        mostrar_listas(id_tablero)


def crear_tarjeta():
    id_tablero = elegir_tablero()
    if id_tablero is None:
        return
    mostrar_listas(id_tablero)
    id_lista = pedir_int("Id de la lista: ")
    if id_lista is None:
        return
    titulo = pedir_texto("Título de la tarjeta: ")
    if not titulo:
        return
    descripcion = pedir_texto("Descripción (opcional): ", False)
    fecha = pedir_fecha("Fecha límite AAAA-MM-DD (opcional): ")
    estado = pedir_texto("Estado (Enter = Pendiente): ", False) or 'Pendiente'
    id_nuevo = servicio.crear_tarjeta(id_lista, titulo, descripcion, fecha, estado)
    if id_nuevo:
        print(f"Tarjeta creada con id {id_nuevo}.")


def listar_tarjetas():
    id_tablero = elegir_tablero()
    if id_tablero is None:
        return
    mostrar_listas(id_tablero)
    id_lista = pedir_int("Id de la lista: ")
    if id_lista is not None:
        mostrar_tarjetas(id_lista)


def mover_tarjeta():
    id_tablero = elegir_tablero()
    if id_tablero is None:
        return
    listas = mostrar_listas(id_tablero)
    for l in listas:
        mostrar_tarjetas(l.id_lista)
    id_tarjeta = pedir_int("Id de la tarjeta a mover: ")
    id_destino = pedir_int("Id de la lista destino: ")
    if id_tarjeta is None or id_destino is None:
        return
    if servicio.mover_tarjeta(id_tarjeta, id_destino):
        print("Tarjeta movida.")
    else:
        print("No se pudo mover la tarjeta.")


def cambiar_estado():
    id_tarjeta = pedir_int("Id tarjeta: ")
    if id_tarjeta is None:
        return
    estado = pedir_texto("Nuevo estado (ej: Pendiente, En progreso, Terminada): ")
    if not estado:
        return
    if servicio.cambiar_estado(id_tarjeta, estado):
        print("Estado actualizado.")
    else:
        print("No se encontró la tarjeta.")


def asignar_tarjeta():
    id_tarjeta = pedir_int("Idtarjeta: ")
    if id_tarjeta is None:
        return
    mostrar_usuarios()
    id_usuario = pedir_int("Id del usuario: ")
    if id_usuario is None:
        return
    if servicio.asignar_tarjeta(id_tarjeta, id_usuario):
        print("Tarjeta asignada.")


def comentar_tarjeta():
    id_tarjeta = pedir_int("Idtarjeta: ")
    if id_tarjeta is None:
        return
    mostrar_usuarios()
    id_usuario = pedir_int("Id del usuario que comenta: ")
    if id_usuario is None:
        return
    texto = pedir_texto("Comentario: ")
    if not texto:
        return
    if servicio.comentar(id_tarjeta, id_usuario, texto):
        print("Comentario agregado.")


def ver_comentarios():
    id_tarjeta = pedir_int("Id de la tarjeta: ")
    if id_tarjeta is None:
        return
    comentarios = servicio.listar_comentarios(id_tarjeta)
    print("\nComentarios:")
    if not comentarios:
        print("  (no hay comentarios)")
    for nombre, texto, fecha in comentarios:
        print(f"  {fecha} - {nombre}: {texto}")


def crear_etiqueta():
    nombre = pedir_texto("Nombre de la etiqueta: ")
    if not nombre:
        return
    color = pedir_texto("Color (ej: rojo): ")
    if not color:
        return
    id_nuevo = servicio.crear_etiqueta(nombre, color)
    if id_nuevo:
        print(f"Etiqueta creada con id {id_nuevo}.")


def etiquetar_tarjeta():
    id_tarjeta = pedir_int("Id de la tarjeta: ")
    if id_tarjeta is None:
        return
    if not mostrar_etiquetas():
        return
    id_etiqueta = pedir_int("Id de la etiqueta: ")
    if id_etiqueta is None:
        return
    if servicio.etiquetar_tarjeta(id_tarjeta, id_etiqueta):
        print("Etiqueta agregada a la tarjeta.")


def gestionar_tareas():
    opciones = {
        '1': 'Crear lista',
        '2': 'Listar listas',
        '3': 'Crear tarjeta',
        '4': 'Listar tarjetas de una lista',
        '5': 'Mover tarjeta a otra lista',
        '6': 'Cambiar estado de tarjeta',
        '7': 'Asignar tarjeta a usuario',
        '8': 'Comentar tarjeta',
        '9': 'Ver comentarios de tarjeta',
        '10': 'Crear etiqueta',
        '11': 'Etiquetar tarjeta',
        '0': 'Volver'
    }
    acciones = {
        '1': crear_lista,
        '2': listar_listas,
        '3': crear_tarjeta,
        '4': listar_tarjetas,
        '5': mover_tarjeta,
        '6': cambiar_estado,
        '7': asignar_tarjeta,
        '8': comentar_tarjeta,
        '9': ver_comentarios,
        '10': crear_etiqueta,
        '11': etiquetar_tarjeta
    }
    ejecutar_submenu("Gestión de Tareas", opciones, acciones)


# ---------- Usuarios ----------
def crear_usuario():
    nombre = pedir_texto("Nombre: ")
    if not nombre:
        return
    email = pedir_texto("Email: ")
    if not email:
        return
    id_nuevo = servicio.crear_usuario(nombre, email)
    if id_nuevo:
        print(f"Usuario creado con id {id_nuevo}.")


def agregar_usuario_proyecto():
    mostrar_proyectos()
    id_proyecto = pedir_int("Id del proyecto: ")
    if id_proyecto is None:
        return
    mostrar_usuarios()
    id_usuario = pedir_int("Id del usuario: ")
    if id_usuario is None:
        return
    rol = pedir_texto("Rol (ej: Administrador, Miembro): ")
    if not rol:
        return
    if servicio.agregar_usuario_proyecto(id_proyecto, id_usuario, rol):
        print("Usuario agregado al proyecto.")


def gestionar_usuarios():
    opciones = {
        '1': 'Crear usuario',
        '2': 'Listar usuarios',
        '3': 'Agregar usuario a un proyecto',
        '0': 'Volver'
    }
    acciones = {
        '1': crear_usuario,
        '2': mostrar_usuarios,
        '3': agregar_usuario_proyecto
    }
    ejecutar_submenu("Gestión de Usuarios", opciones, acciones)


# ---------- Reportes ----------
def reporte_avance():
    mostrar_proyectos()
    id_proyecto = pedir_int("Id del proyecto: ")
    if id_proyecto is None:
        return
    datos = servicio.reporte_avance(id_proyecto)
    print("\nAvance del proyecto (tarjetas por estado):")
    if not datos:
        print("  (el proyecto no tiene tarjetas)")
    total = sum(cantidad for _, cantidad in datos)
    for estado, cantidad in datos:
        porcentaje = cantidad * 100 / total
        print(f"  {estado or 'Sin estado'}: {cantidad} ({porcentaje:.0f}%)")


def reporte_por_usuario():
    datos = servicio.reporte_tarjetas_por_usuario()
    print("\nTarjetas asignadas por usuario:")
    if not datos:
        print("  (no hay usuarios)")
    for nombre, cantidad in datos:
        print(f"  {nombre}: {cantidad}")


def gestionar_reportes():
    opciones = {
        '1': 'Avance de un proyecto',
        '2': 'Tarjetas asignadas por usuario',
        '0': 'Volver'
    }
    acciones = {
        '1': reporte_avance,
        '2': reporte_por_usuario
    }
    ejecutar_submenu("Reportes", opciones, acciones)


# ---------- Menú principal ----------
def cargar_menu():
    opciones = {
        '1': 'Gestión de Proyectos',
        '2': 'Gestión de Tareas',
        '3': 'Gestión de Usuarios',
        '4': 'Reportes',
        '5': 'Ver tablas de la base de datos',
        '6': 'Salir'
    }
    acciones = {
        '1': gestionar_proyectos,
        '2': gestionar_tareas,
        '3': gestionar_usuarios,
        '4': gestionar_reportes,
        '5': mostrar_tablas
    }
    while True:
        mostrar_menu(f"{nombre_app} - v{version_app}", opciones)
        opcion = input("Selecciona una opción: ").strip()
        if opcion == '6':
            print("Saliendo...")
            break
        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida, intenta de nuevo.")
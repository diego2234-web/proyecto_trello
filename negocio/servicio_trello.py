from peewee import fn, JOIN
from REPOSITORIO.models import (
    db, Proyecto, Usuario, ProyectoUsuario, Tablero, Lista, Tarjeta,
    Comentario, Etiqueta, AsignacionTarjeta, TarjetaEtiqueta
)


class ServicioTrello:

    def _ejecutar(self, accion, defecto=None):
        """Abre y cierra la conexión, y aísla los errores."""
        try:
            with db.connection_context():
                return accion()
        except Exception as e:
            print(f"Error: {e}")
            return defecto

    # ---------- General ----------
    def listar_tablas(self):
        return self._ejecutar(lambda: db.get_tables(), [])

    # ---------- Proyectos ----------
    def crear_proyecto(self, nombre, descripcion=None):
        return self._ejecutar(
            lambda: Proyecto.create(
                nombre_proyecto=nombre, descripcion=descripcion
            ).id_proyecto
        )

    def listar_proyectos(self):
        return self._ejecutar(
            lambda: list(Proyecto.select().order_by(Proyecto.id_proyecto)), []
        )

    # ---------- Tableros ----------
    def crear_tablero(self, id_proyecto, titulo):
        return self._ejecutar(
            lambda: Tablero.create(
                proyecto=id_proyecto, titulo=titulo
            ).id_tablero
        )

    def listar_tableros(self, id_proyecto=None):
        def accion():
            q = Tablero.select().order_by(Tablero.id_tablero)
            if id_proyecto:
                q = q.where(Tablero.proyecto == id_proyecto)
            return list(q)
        return self._ejecutar(accion, [])

    # ---------- Listas ----------
    def crear_lista(self, id_tablero, nombre_lista):
        def accion():
            ultima = Lista.select(fn.MAX(Lista.posicion)).where(
                Lista.tablero == id_tablero
            ).scalar() or 0
            return Lista.create(
                tablero=id_tablero,
                nombre_lista=nombre_lista,
                posicion=ultima + 1
            ).id_lista
        return self._ejecutar(accion)

    def listar_listas(self, id_tablero):
        return self._ejecutar(
            lambda: list(
                Lista.select()
                .where(Lista.tablero == id_tablero)
                .order_by(Lista.posicion)
            ), []
        )

    # ---------- Tarjetas ----------
    def crear_tarjeta(self, id_lista, titulo, descripcion=None,
                      fecha_limite=None, estado='Pendiente'):
        return self._ejecutar(
            lambda: Tarjeta.create(
                lista=id_lista, titulo=titulo, descripcion=descripcion,
                fecha_limite=fecha_limite, estado=estado
            ).id_tarjeta
        )

    def listar_tarjetas(self, id_lista):
        return self._ejecutar(
            lambda: list(
                Tarjeta.select()
                .where(Tarjeta.lista == id_lista)
                .order_by(Tarjeta.id_tarjeta)
            ), []
        )

    def mover_tarjeta(self, id_tarjeta, id_lista_destino):
        return self._ejecutar(
            lambda: Tarjeta.update(lista=id_lista_destino)
            .where(Tarjeta.id_tarjeta == id_tarjeta).execute(), 0
        )

    def cambiar_estado(self, id_tarjeta, estado):
        return self._ejecutar(
            lambda: Tarjeta.update(estado=estado)
            .where(Tarjeta.id_tarjeta == id_tarjeta).execute(), 0
        )

    # ---------- Usuarios ----------
    def crear_usuario(self, nombre, email):
        return self._ejecutar(
            lambda: Usuario.create(nombre=nombre, email=email).id_usuario
        )

    def listar_usuarios(self):
        return self._ejecutar(
            lambda: list(Usuario.select().order_by(Usuario.id_usuario)), []
        )

    def agregar_usuario_proyecto(self, id_proyecto, id_usuario, rol):
        def accion():
            ProyectoUsuario.create(
                proyecto=id_proyecto, usuario=id_usuario, rol=rol
            )
            return True
        return self._ejecutar(accion, False)

    def asignar_tarjeta(self, id_tarjeta, id_usuario):
        def accion():
            AsignacionTarjeta.create(tarjeta=id_tarjeta, usuario=id_usuario)
            return True
        return self._ejecutar(accion, False)

    # ---------- Comentarios ----------
    def comentar(self, id_tarjeta, id_usuario, texto):
        return self._ejecutar(
            lambda: Comentario.create(
                tarjeta=id_tarjeta, usuario=id_usuario, texto=texto
            ).id_comentario
        )

    def listar_comentarios(self, id_tarjeta):
        return self._ejecutar(
            lambda: list(
                Comentario.select(
                    Usuario.nombre, Comentario.texto, Comentario.fecha_creacion
                )
                .join(Usuario)
                .where(Comentario.tarjeta == id_tarjeta)
                .order_by(Comentario.fecha_creacion)
                .tuples()
            ), []
        )

    # ---------- Etiquetas ----------
    def crear_etiqueta(self, nombre, color):
        return self._ejecutar(
            lambda: Etiqueta.create(nombre=nombre, color=color).id_etiqueta
        )

    def listar_etiquetas(self):
        return self._ejecutar(
            lambda: list(Etiqueta.select().order_by(Etiqueta.id_etiqueta)), []
        )

    def etiquetar_tarjeta(self, id_tarjeta, id_etiqueta):
        def accion():
            TarjetaEtiqueta.create(tarjeta=id_tarjeta, etiqueta=id_etiqueta)
            return True
        return self._ejecutar(accion, False)

    # ---------- Reportes ----------
    def reporte_avance(self, id_proyecto):
        return self._ejecutar(
            lambda: list(
                Tarjeta.select(Tarjeta.estado, fn.COUNT(Tarjeta.id_tarjeta))
                .join(Lista)
                .join(Tablero)
                .where(Tablero.proyecto == id_proyecto)
                .group_by(Tarjeta.estado)
                .tuples()
            ), []
        )

    def reporte_tarjetas_por_usuario(self):
        return self._ejecutar(
            lambda: list(
                Usuario.select(
                    Usuario.nombre, fn.COUNT(AsignacionTarjeta.tarjeta)
                )
                .join(AsignacionTarjeta, JOIN.LEFT_OUTER)
                .group_by(Usuario.id_usuario, Usuario.nombre)
                .tuples()
            ), []
        )

# auxiliares/seguridad.py
import bcrypt


def hashear_contrasena(contrasena: str) -> str:
    # bcrypt hashea (no se puede desencriptar), que es lo correcto para contraseñas
    return bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_contrasena(contrasena: str, hash_guardado: str) -> bool:
    return bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("utf-8"))

from pathlib import Path
import sqlite3

from werkzeug.security import generate_password_hash


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"


USUARIOS_DEFINITIVOS = (
    (
        "María José Ledezma",
        "majo l",
        "Majo123",
        "administrador",
    ),
    (
        "Daniela Delgado",
        "dani dg",
        "Dani123",
        "administrador",
    ),
    (
        "Diego Carrillo Guevara",
        "diego c.",
        "Diego123",
        "usuario",
    ),
    (
        "Lucia Viales Elizondo",
        "lucia v.",
        "Lu123",
        "visitante",
    ),
)


def actualizar_usuarios() -> None:
    if not RUTA_BASE_DATOS.exists():
        print(f"ERROR: No se encontró la base de datos:\n{RUTA_BASE_DATOS}")
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'usuarios'
            """
        )

        if cursor.fetchone() is None:
            raise RuntimeError(
                "La tabla usuarios no existe. "
                "Primero ejecutá crear_usuarios.py."
            )

        # Elimina las cuentas provisionales y cualquier usuario anterior.
        cursor.execute("DELETE FROM usuarios")

        for nombre, nombre_usuario, contrasena, rol in USUARIOS_DEFINITIVOS:
            cursor.execute(
                """
                INSERT INTO usuarios (
                    nombre,
                    nombre_usuario,
                    contrasena_hash,
                    rol,
                    activo
                )
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    nombre,
                    nombre_usuario,
                    generate_password_hash(contrasena),
                    rol,
                ),
            )

        conexion.commit()

        cursor.execute(
            """
            SELECT
                nombre,
                nombre_usuario,
                rol,
                activo
            FROM usuarios
            ORDER BY
                CASE rol
                    WHEN 'administrador' THEN 1
                    WHEN 'usuario' THEN 2
                    WHEN 'visitante' THEN 3
                END,
                nombre
            """
        )

        usuarios = cursor.fetchall()

        print("\n" + "=" * 72)
        print("USUARIOS DE BIOTRACK ACTUALIZADOS CORRECTAMENTE")
        print("=" * 72)

        for nombre, nombre_usuario, rol, activo in usuarios:
            estado = "Activo" if activo == 1 else "Inactivo"

            print(
                f"{nombre} | "
                f"{nombre_usuario} | "
                f"{rol} | "
                f"{estado}"
            )

        print("=" * 72)
        print("Los equipos y demás datos no fueron modificados.")
        print("=" * 72)

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()

        print("\nERROR AL ACTUALIZAR LOS USUARIOS")
        print(error)
        print("No se guardaron cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    actualizar_usuarios()
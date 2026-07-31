from pathlib import Path
import sqlite3

from werkzeug.security import generate_password_hash


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"


USUARIOS_INICIALES = (
    (
        "Administrador BioTrack",
        "admin",
        "Admin123!",
        "administrador",
    ),
    (
        "Usuario BioTrack",
        "usuario",
        "Usuario123!",
        "usuario",
    ),
    (
        "Visitante BioTrack",
        "visitante",
        "Visitante123!",
        "visitante",
    ),
)


def crear_tabla_usuarios() -> None:
    if not RUTA_BASE_DATOS.exists():
        print(f"ERROR: No se encontró la base de datos:\n{RUTA_BASE_DATOS}")
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                nombre_usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL,
                rol TEXT NOT NULL
                    CHECK (
                        rol IN (
                            'administrador',
                            'usuario',
                            'visitante'
                        )
                    ),
                activo INTEGER NOT NULL DEFAULT 1
                    CHECK (activo IN (0, 1)),
                fecha_creacion TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso TEXT
            )
            """
        )

        for nombre, nombre_usuario, contrasena, rol in USUARIOS_INICIALES:
            cursor.execute(
                """
                INSERT OR IGNORE INTO usuarios (
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
            SELECT id, nombre, nombre_usuario, rol, activo
            FROM usuarios
            ORDER BY id
            """
        )
        usuarios = cursor.fetchall()

        print("\n" + "=" * 68)
        print("TABLA DE USUARIOS CREADA CORRECTAMENTE")
        print("=" * 68)

        for usuario in usuarios:
            estado = "Activo" if usuario[4] == 1 else "Inactivo"

            print(
                f"{usuario[0]} | "
                f"{usuario[1]} | "
                f"{usuario[2]} | "
                f"{usuario[3]} | "
                f"{estado}"
            )

        print("=" * 68)
        print("Los equipos y demás tablas no fueron modificados.")

    except sqlite3.Error as error:
        conexion.rollback()
        print("\nERROR AL CREAR LA TABLA DE USUARIOS")
        print(error)
        print("No se guardaron cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tabla_usuarios()
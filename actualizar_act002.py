from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-002"


def actualizar_act002() -> None:
    if not RUTA_BASE_DATOS.exists():
        print(f"ERROR: No se encontró la base de datos:\n{RUTA_BASE_DATOS}")
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT 1 FROM equipos WHERE activo = ?",
            (ACTIVO,),
        )

        if cursor.fetchone() is None:
            raise RuntimeError("No existe el equipo ACT-002.")

        # Quitar referencia a datos simulados.
        cursor.execute(
            """
            UPDATE equipos
            SET observaciones = ?
            WHERE activo = ?
            """,
            (
                (
                    "Equipo destinado a reanimación, desfibrilación, "
                    "cardioversión sincronizada y monitoreo durante emergencias. "
                    "Se encuentra disponible para uso clínico."
                ),
                ACTIVO,
            ),
        )

        # Quitar versiones académicas o simuladas.
        cursor.execute(
            """
            UPDATE configuracion
            SET
                version_software = ?,
                version_firmware = ?,
                idioma = ?,
                conectividad = ?
            WHERE activo = ?
            """,
            (
                "3.2",
                "2.8",
                "Español",
                "USB, red hospitalaria y exportación de eventos",
                ACTIVO,
            ),
        )

        # Quitar referencia a registro simulado.
        cursor.execute(
            """
            UPDATE informacion_regulatoria
            SET
                registro_sanitario = ?,
                fda = ?,
                norma = ?,
                clasificacion_riesgo = ?
            WHERE activo = ?
            """,
            (
                "Consultar documentación regulatoria vigente",
                "Conforme a la documentación del fabricante",
                "IEC 60601-1 / IEC 60601-2-4",
                "Clase IIb",
                ACTIVO,
            ),
        )

        conexion.commit()

        print("\n" + "=" * 68)
        print("ACT-002 ACTUALIZADO CORRECTAMENTE")
        print("=" * 68)
        print("Se eliminaron las referencias a datos simulados y académicos.")
        print("Los demás activos no fueron modificados.")
        print("=" * 68)

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR AL ACTUALIZAR EL ACT-002")
        print(error)
        print("No se guardaron cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    actualizar_act002()
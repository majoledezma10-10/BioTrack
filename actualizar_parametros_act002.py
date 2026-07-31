from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-002"


def actualizar_parametros_act002() -> None:
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

        cursor.execute(
            "DELETE FROM parametros_monitorizados WHERE activo = ?",
            (ACTIVO,),
        )

        cursor.execute(
            """
            INSERT INTO parametros_monitorizados (
                activo,
                ecg,
                frecuencia_cardiaca,
                frecuencia_respiratoria,
                spo2,
                nibp,
                temperatura,
                ibp,
                etco2
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ACTIVO,
                "Energía seleccionable de 2 a 200 Joules en modo manual.",
                (
                    "Modo AED con energía preestablecida de 150 Joules, "
                    "sin escalonamiento."
                ),
                (
                    "Forma de onda bifásica exponencial truncada, ajustada "
                    "automáticamente según la impedancia del paciente."
                ),
                "Carga a 200 Joules en menos de 3 segundos.",
                (
                    "Marcapasos opcional: frecuencia de 30 a 180 ppm, "
                    "en incrementos de 10 ppm y precisión de ±1.5 %."
                ),
                "Cardioversión sincronizada disponible.",
                "No aplica",
                "No aplica",
            ),
        )

        conexion.commit()

        print("\n" + "=" * 65)
        print("PARÁMETROS DEL ACT-002 ACTUALIZADOS CORRECTAMENTE")
        print("=" * 65)
        print("Los demás equipos y secciones no fueron modificados.")
        print("=" * 65)

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR AL ACTUALIZAR EL ACT-002")
        print(error)
        print("No se guardaron cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    actualizar_parametros_act002()
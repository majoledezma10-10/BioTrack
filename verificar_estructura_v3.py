import sqlite3
from pathlib import Path


RUTA_BASE_DATOS = Path("database/biotrack_v2.db")


def mostrar_estructura():
    if not RUTA_BASE_DATOS.exists():
        print(f"ERROR: No se encontró la base de datos: {RUTA_BASE_DATOS}")
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tablas = cursor.fetchall()

    if not tablas:
        print("No se encontraron tablas en la base de datos.")
        conexion.close()
        return

    print("=" * 70)
    print("ESTRUCTURA DE BIOTRACK V3")
    print("=" * 70)

    for (nombre_tabla,) in tablas:
        print(f"\nTABLA: {nombre_tabla}")
        print("-" * 70)

        cursor.execute(f'PRAGMA table_info("{nombre_tabla}")')
        columnas = cursor.fetchall()

        for columna in columnas:
            identificador = columna[0]
            nombre = columna[1]
            tipo = columna[2]
            obligatorio = "Sí" if columna[3] else "No"
            valor_default = columna[4]
            llave_primaria = "Sí" if columna[5] else "No"

            print(
                f"ID: {identificador} | "
                f"Columna: {nombre} | "
                f"Tipo: {tipo or 'Sin tipo'} | "
                f"Obligatoria: {obligatorio} | "
                f"Default: {valor_default} | "
                f"PK: {llave_primaria}"
            )

        cursor.execute(f'SELECT COUNT(*) FROM "{nombre_tabla}"')
        cantidad = cursor.fetchone()[0]
        print(f"Registros actuales: {cantidad}")

    conexion.close()

    print("\n" + "=" * 70)
    print("VERIFICACIÓN FINALIZADA")
    print("=" * 70)


if __name__ == "__main__":
    mostrar_estructura()
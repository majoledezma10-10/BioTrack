import sqlite3

conexion = sqlite3.connect("database/biotrack_v2.db")
conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

activo = "ACT-001"

tablas = [
    "equipos",
    "informacion_tecnica",
    "parametros_monitorizados",
    "configuracion",
    "informacion_regulatoria",
    "mantenimientos",
    "calibraciones",
    "fallas",
    "indicadores",
    "informacion_economica",
    "documentos"
]

print(f"Verificación del equipo {activo}\n")

for tabla in tablas:
    cursor.execute(
        f"SELECT COUNT(*) AS cantidad FROM {tabla} WHERE activo = ?",
        (activo,)
    )
    cantidad = cursor.fetchone()["cantidad"]
    print(f"{tabla}: {cantidad} registro(s)")

conexion.close()
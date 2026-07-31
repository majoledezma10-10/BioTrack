import sqlite3

conexion = sqlite3.connect("database/biotrack.db")
cursor = conexion.cursor()

cursor.execute("""
INSERT OR REPLACE INTO equipos (
    activo,
    nombre_equipo,
    marca,
    modelo,
    serie,
    ubicacion,
    estado,
    fecha_ingreso,
    observaciones
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "ACT-001",
    "Monitor de Signos Vitales",
    "Philips",
    "MX450",
    "SN-12345",
    "UCI",
    "Operativo",
    "10/06/2026",
    "Equipo en buen estado general."
))

conexion.commit()
conexion.close()

print("Equipo insertado correctamente")
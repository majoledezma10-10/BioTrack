import sqlite3

# Crear conexión con la base de datos
conexion = sqlite3.connect("database/biotrack.db")

cursor = conexion.cursor()

# Tabla de equipos
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    activo TEXT PRIMARY KEY,
    nombre_equipo TEXT,
    marca TEXT,
    modelo TEXT,
    serie TEXT,
    ubicacion TEXT,
    estado TEXT,
    fecha_ingreso TEXT,
    observaciones TEXT
)
""")

# Tabla de historial
cursor.execute("""
CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT,
    fecha TEXT,
    tipo_evento TEXT,
    descripcion TEXT,
    tecnico_responsable TEXT,
    repuestos_utilizados TEXT,
    proximo_mantenimiento TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")
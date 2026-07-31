import sqlite3

# Crear o abrir la nueva base de datos
conexion = sqlite3.connect("database/biotrack_v2.db")

# Activar las relaciones entre las tablas
conexion.execute("PRAGMA foreign_keys = ON")

cursor = conexion.cursor()

# Crear la tabla principal de equipos
cursor.execute("""
CREATE TABLE IF NOT EXISTS equipos (
    activo TEXT PRIMARY KEY,
    codigo_qr TEXT UNIQUE,
    nombre TEXT NOT NULL,
    tipo_equipo TEXT,
    marca TEXT,
    modelo TEXT,
    serie TEXT,
    fabricante TEXT,
    pais_fabricacion TEXT,
    anio_fabricacion INTEGER,
    fecha_compra TEXT,
    fecha_ingreso TEXT,
    ubicacion TEXT,
    servicio TEXT,
    responsable TEXT,
    estado TEXT,
    criticidad TEXT,
    vida_util_estimada TEXT,
    observaciones TEXT
)
""")
# Crear la tabla de información técnica
cursor.execute("""
CREATE TABLE IF NOT EXISTS informacion_tecnica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    voltaje_alimentacion TEXT,
    tipo_bateria TEXT,
    capacidad_bateria TEXT,
    grado_proteccion_ip TEXT,
    peso TEXT,
    dimensiones TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de parámetros monitorizados
cursor.execute("""
CREATE TABLE IF NOT EXISTS parametros_monitorizados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    ecg TEXT,
    frecuencia_cardiaca TEXT,
    frecuencia_respiratoria TEXT,
    spo2 TEXT,
    nibp TEXT,
    temperatura TEXT,
    ibp TEXT,
    etco2 TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de configuración
cursor.execute("""
CREATE TABLE IF NOT EXISTS configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    version_software TEXT,
    version_firmware TEXT,
    idioma TEXT,
    conectividad TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de información regulatoria
cursor.execute("""
CREATE TABLE IF NOT EXISTS informacion_regulatoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    registro_sanitario TEXT,
    fda TEXT,
    norma TEXT,
    clasificacion_riesgo TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de mantenimientos
cursor.execute("""
CREATE TABLE IF NOT EXISTS mantenimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT NOT NULL,
    fecha TEXT,
    tipo TEXT,
    tecnico_responsable TEXT,
    descripcion TEXT,
    repuestos_utilizados TEXT,
    proximo_mantenimiento TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de calibraciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS calibraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT NOT NULL,
    fecha TEXT,
    resultado TEXT,
    certificado TEXT,
    patron_utilizado TEXT,
    proxima_calibracion TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de historial de fallas
cursor.execute("""
CREATE TABLE IF NOT EXISTS fallas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT NOT NULL,
    fecha TEXT,
    falla_reportada TEXT,
    diagnostico TEXT,
    accion_realizada TEXT,
    tiempo_fuera_servicio TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de indicadores del equipo
cursor.execute("""
CREATE TABLE IF NOT EXISTS indicadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    disponibilidad TEXT,
    horas_operacion TEXT,
    mantenimientos_preventivos INTEGER,
    mantenimientos_correctivos INTEGER,
    calibraciones INTEGER,
    tiempo_fuera_servicio TEXT,
    mtbf TEXT,
    mttr TEXT,
    cumplimiento_mantenimiento TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de información económica
cursor.execute("""
CREATE TABLE IF NOT EXISTS informacion_economica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    costo_adquisicion REAL,
    garantia TEXT,
    vencimiento_garantia TEXT,
    costo_mantenimiento_preventivo REAL,
    costo_reparaciones REAL,
    costo_total_repuestos REAL,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla de documentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    manual_usuario TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
# Crear la tabla del código QR
cursor.execute("""
CREATE TABLE IF NOT EXISTS codigo_qr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activo TEXT UNIQUE,
    codigo_qr TEXT,
    FOREIGN KEY (activo) REFERENCES equipos(activo)
)
""")
conexion.commit()
conexion.close()

print("Base de datos BioTrack V2 creada correctamente")
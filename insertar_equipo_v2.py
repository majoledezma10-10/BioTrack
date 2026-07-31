import sqlite3

# Conectarse a la nueva base de datos
conexion = sqlite3.connect("database/biotrack_v2.db")

cursor = conexion.cursor()
# Activar las relaciones entre tablas
conexion.execute("PRAGMA foreign_keys = ON")

# Insertar la información general del equipo
cursor.execute("""
INSERT INTO equipos (
    activo,
    codigo_qr,
    nombre,
    tipo_equipo,
    marca,
    modelo,
    serie,
    fabricante,
    pais_fabricacion,
    anio_fabricacion,
    fecha_compra,
    fecha_ingreso,
    ubicacion,
    servicio,
    responsable,
    estado,
    criticidad,
    vida_util_estimada,
    observaciones
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    codigo_qr = excluded.codigo_qr,
    nombre = excluded.nombre,
    tipo_equipo = excluded.tipo_equipo,
    marca = excluded.marca,
    modelo = excluded.modelo,
    serie = excluded.serie,
    fabricante = excluded.fabricante,
    pais_fabricacion = excluded.pais_fabricacion,
    anio_fabricacion = excluded.anio_fabricacion,
    fecha_compra = excluded.fecha_compra,
    fecha_ingreso = excluded.fecha_ingreso,
    ubicacion = excluded.ubicacion,
    servicio = excluded.servicio,
    responsable = excluded.responsable,
    estado = excluded.estado,
    criticidad = excluded.criticidad,
    vida_util_estimada = excluded.vida_util_estimada,
    observaciones = excluded.observaciones
""", (
    "ACT-001",
    "QR-ACT001",
    "Monitor de Signos Vitales",
    "Monitor Multiparámetro",
    "Philips",
    "IntelliVue MX450",
    "MX450-20-483721",
    "Philips Healthcare",
    "Estados Unidos",
    2020,
    "15/02/2021",
    "03/03/2021",
    "Unidad de Cuidados Intensivos (UCI)",
    "Medicina Crítica",
    "Jefatura de Enfermería UCI",
    "Operativo",
    "Alta",
    "10 años",
    "Equipo en excelente estado de funcionamiento. Sin daños físicos visibles."
))
# Insertar la información técnica
cursor.execute("""
INSERT INTO informacion_tecnica (
    activo,
    voltaje_alimentacion,
    tipo_bateria,
    capacidad_bateria,
    grado_proteccion_ip,
    peso,
    dimensiones
)
VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    voltaje_alimentacion = excluded.voltaje_alimentacion,
    tipo_bateria = excluded.tipo_bateria,
    capacidad_bateria = excluded.capacidad_bateria,
    grado_proteccion_ip = excluded.grado_proteccion_ip,
    peso = excluded.peso,
    dimensiones = excluded.dimensiones
""", (
    "ACT-001",
    "100–240 VAC",
    "Ion-Litio recargable",
    "6600 mAh",
    "IPX1",
    "5.8 kg",
    "310 × 250 × 160 mm"
))
# Insertar los parámetros monitorizados
cursor.execute("""
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
ON CONFLICT(activo) DO UPDATE SET
    ecg = excluded.ecg,
    frecuencia_cardiaca = excluded.frecuencia_cardiaca,
    frecuencia_respiratoria = excluded.frecuencia_respiratoria,
    spo2 = excluded.spo2,
    nibp = excluded.nibp,
    temperatura = excluded.temperatura,
    ibp = excluded.ibp,
    etco2 = excluded.etco2
""", (
    "ACT-001",
    "Disponible",
    "Disponible",
    "Disponible",
    "Disponible",
    "Disponible",
    "Disponible",
    "Disponible",
    "Disponible"
))
# Insertar la configuración del equipo
cursor.execute("""
INSERT INTO configuracion (
    activo,
    version_software,
    version_firmware,
    idioma,
    conectividad
)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    version_software = excluded.version_software,
    version_firmware = excluded.version_firmware,
    idioma = excluded.idioma,
    conectividad = excluded.conectividad
""", (
    "ACT-001",
    "J.00.33",
    "5.2.1",
    "Español",
    "LAN / Wi-Fi"
))
# Insertar la información regulatoria
cursor.execute("""
INSERT INTO informacion_regulatoria (
    activo,
    registro_sanitario,
    fda,
    norma,
    clasificacion_riesgo
)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    registro_sanitario = excluded.registro_sanitario,
    fda = excluded.fda,
    norma = excluded.norma,
    clasificacion_riesgo = excluded.clasificacion_riesgo
""", (
    "ACT-001",
    "Vigente",
    "Aprobado",
    "IEC 60601-1",
    "Clase IIb"
))
# Eliminar mantenimientos anteriores del ACT-001 para evitar duplicados
cursor.execute(
    "DELETE FROM mantenimientos WHERE activo = ?",
    ("ACT-001",)
)

# Historial de mantenimientos del equipo
mantenimientos = [
    ("ACT-001", "15/09/2021", "Preventivo", "Luis Rodríguez",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "18/03/2022", "Preventivo", "Luis Rodríguez",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "25/05/2022", "Correctivo", "Carlos Jiménez",
     "Cambio de batería interna.", "Batería original Philips", None),

    ("ACT-001", "12/09/2022", "Preventivo", "Carlos Jiménez",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "20/03/2023", "Preventivo", "Andrés Mora",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "19/09/2023", "Preventivo", "Andrés Mora",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "06/11/2023", "Correctivo", "Sofía Vargas",
     "Sustitución de cable ECG de 5 derivaciones y pruebas funcionales.",
     "Cable ECG de 5 derivaciones", None),

    ("ACT-001", "15/03/2024", "Preventivo", "Sofía Vargas",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "17/09/2024", "Preventivo", "Sofía Vargas",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "15/12/2024", "Correctivo", "Sofía Vargas",
     "Sustitución del sensor de temperatura y pruebas funcionales.",
     "Sensor de temperatura", None),

    ("ACT-001", "14/03/2025", "Preventivo", "José Hernández",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "16/09/2025", "Preventivo", "José Hernández",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno", None),

    ("ACT-001", "17/03/2026", "Preventivo", "María González",
     "Mantenimiento realizado. Resultado conforme.", "Ninguno",
     "17/09/2026")
]

cursor.executemany("""
INSERT INTO mantenimientos (
    activo,
    fecha,
    tipo,
    tecnico_responsable,
    descripcion,
    repuestos_utilizados,
    proximo_mantenimiento
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", mantenimientos)
# Eliminar calibraciones anteriores para evitar duplicados
cursor.execute(
    "DELETE FROM calibraciones WHERE activo = ?",
    ("ACT-001",)
)

# Historial de calibraciones
calibraciones = [
    ("ACT-001", "15/09/2021", "Conforme", "CAL-2021-081",
     "Fluke ProSim 8", None),

    ("ACT-001", "18/03/2022", "Conforme", "CAL-2022-034",
     "Fluke ProSim 8", None),

    ("ACT-001", "20/03/2023", "Conforme", "CAL-2023-067",
     "Fluke ProSim 8", None),

    ("ACT-001", "15/03/2024", "Conforme", "CAL-2024-052",
     "Fluke ProSim 8", None),

    ("ACT-001", "14/03/2025", "Conforme", "CAL-2025-041",
     "Fluke ProSim 8", None),

    ("ACT-001", "17/03/2026", "Conforme", "CAL-2026-036",
     "Fluke ProSim 8", "17/03/2027")
]

cursor.executemany("""
INSERT INTO calibraciones (
    activo,
    fecha,
    resultado,
    certificado,
    patron_utilizado,
    proxima_calibracion
)
VALUES (?, ?, ?, ?, ?, ?)
""", calibraciones)
# Eliminar fallas anteriores para evitar duplicados
cursor.execute(
    "DELETE FROM fallas WHERE activo = ?",
    ("ACT-001",)
)

# Historial de fallas
fallas = [
    (
        "ACT-001",
        "25/05/2022",
        "Baja autonomía de batería.",
        "Batería degradada por uso.",
        "Reemplazo de batería original Philips.",
        "3 horas"
    ),
    (
        "ACT-001",
        "06/11/2023",
        "Lecturas irregulares.",
        "Cables sin continuidad.",
        "Sustitución de cable ECG de 5 derivaciones y pruebas funcionales.",
        "2 horas"
    ),
    (
        "ACT-001",
        "15/12/2024",
        "Lecturas erráticas de temperatura.",
        "Sensor de temperatura deteriorado.",
        "Sustitución del sensor y pruebas funcionales.",
        "2 horas"
    )
]

cursor.executemany("""
INSERT INTO fallas (
    activo,
    fecha,
    falla_reportada,
    diagnostico,
    accion_realizada,
    tiempo_fuera_servicio
)
VALUES (?, ?, ?, ?, ?, ?)
""", fallas)
# Insertar los indicadores del equipo
cursor.execute("""
INSERT INTO indicadores (
    activo,
    disponibilidad,
    horas_operacion,
    mantenimientos_preventivos,
    mantenimientos_correctivos,
    calibraciones,
    tiempo_fuera_servicio,
    mtbf,
    mttr,
    cumplimiento_mantenimiento
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    disponibilidad = excluded.disponibilidad,
    horas_operacion = excluded.horas_operacion,
    mantenimientos_preventivos = excluded.mantenimientos_preventivos,
    mantenimientos_correctivos = excluded.mantenimientos_correctivos,
    calibraciones = excluded.calibraciones,
    tiempo_fuera_servicio = excluded.tiempo_fuera_servicio,
    mtbf = excluded.mtbf,
    mttr = excluded.mttr,
    cumplimiento_mantenimiento = excluded.cumplimiento_mantenimiento
""", (
    "ACT-001",
    "99.3 %",
    "13,800 horas",
    10,
    3,
    6,
    "7 horas",
    "6,900 horas",
    "2.5 horas",
    "100 %"
))
# Insertar la información económica
cursor.execute("""
INSERT INTO informacion_economica (
    activo,
    costo_adquisicion,
    garantia,
    vencimiento_garantia,
    costo_mantenimiento_preventivo,
    costo_reparaciones,
    costo_total_repuestos
)
VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(activo) DO UPDATE SET
    costo_adquisicion = excluded.costo_adquisicion,
    garantia = excluded.garantia,
    vencimiento_garantia = excluded.vencimiento_garantia,
    costo_mantenimiento_preventivo = excluded.costo_mantenimiento_preventivo,
    costo_reparaciones = excluded.costo_reparaciones,
    costo_total_repuestos = excluded.costo_total_repuestos
""", (
    "ACT-001",
    8750.00,
    "3 años",
    "03/03/2024",
    1563.00,
    721.00,
    1500.00
))
# Insertar el manual del usuario
cursor.execute("""
INSERT INTO documentos (
    activo,
    manual_usuario
)
VALUES (?, ?)
ON CONFLICT(activo) DO UPDATE SET
    manual_usuario = excluded.manual_usuario
""", (
    "ACT-001",
    "https://www.documents.philips.com/assets/Instruction%20for%20Use/20260424/83cba6c0fe91400ea93ab436008655e7.pdf?feed=ifu_docs_feed&utm_source"
))

# Guardar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()

print("Información general del ACT-001 guardada correctamente")
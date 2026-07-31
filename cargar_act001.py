from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-001"


def eliminar_registros_existentes(cursor: sqlite3.Cursor) -> None:
    tablas_dependientes = (
        "calibraciones",
        "codigo_qr",
        "configuracion",
        "documentos",
        "fallas",
        "indicadores",
        "informacion_economica",
        "informacion_regulatoria",
        "informacion_tecnica",
        "mantenimientos",
        "parametros_monitorizados",
    )

    for tabla in tablas_dependientes:
        cursor.execute(
            f'DELETE FROM "{tabla}" WHERE activo = ?',
            (ACTIVO,),
        )

    cursor.execute(
        "DELETE FROM equipos WHERE activo = ?",
        (ACTIVO,),
    )


def insertar_act001(cursor: sqlite3.Cursor) -> None:
    # INFORMACIÓN GENERAL
    cursor.execute(
        """
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
        """,
        (
            ACTIVO,
            "QR-ACT001",
            "Monitor de Signos Vitales",
            "Monitor multiparámetro",
            "Philips",
            "IntelliVue MX450",
            "MX450-22-746518",
            "Philips Medical Systems",
            "Estados Unidos",
            2022,
            "2022-08-15",
            "2022-09-05",
            "Unidad de Cuidados Intensivos",
            "UCI Adultos",
            "Jefatura de Enfermería UCI",
            "Operativo",
            "Alta",
            "10 años",
            (
                "Equipo utilizado para monitorización continua "
                "de pacientes críticos."
            ),
        ),
    )

    # INFORMACIÓN TÉCNICA
    cursor.execute(
        """
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
        """,
        (
            ACTIVO,
            "100-240 VAC, 50/60 Hz",
            "Ion-litio recargable",
            (
                "Autonomía aproximada de 5 horas. Pantalla TFT LCD "
                "táctil a color de 12.1 pulgadas, resolución 1280 × 800 píxeles."
            ),
            "IPX1; protección eléctrica Clase I",
            "5.8 kg",
            (
                "Conectividad LAN, WLAN opcional e integración "
                "con IntelliVue Network"
            ),
        ),
    )

    # PARÁMETROS MONITORIZADOS
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
            (
                "ECG de 3, 5, 6 y 10 derivaciones. Análisis de arritmias, "
                "análisis del segmento ST y medición QT/QTc disponibles."
            ),
            "Frecuencia cardíaca: 15 a 300 lpm.",
            (
                "Respiración por impedancia disponible. "
                "Frecuencia respiratoria: 3 a 150 respiraciones/min."
            ),
            (
                "SpO₂ y pulso disponibles mediante módulo compatible."
            ),
            (
                "Presión arterial no invasiva disponible."
            ),
            (
                "Temperatura de hasta 2 canales. Gases anestésicos, "
                "gasto cardíaco, BIS, EEG/aEEG y NMT disponibles "
                "según módulos instalados."
            ),
            (
                "Presión invasiva de hasta 2 canales, "
                "según la configuración del equipo."
            ),
            (
                "Capnografía EtCO₂ opcional. Guardian Early Warning Score "
                "disponible."
            ),
        ),
    )

    # CONFIGURACIÓN
    cursor.execute(
        """
        INSERT INTO configuracion (
            activo,
            version_software,
            version_firmware,
            idioma,
            conectividad
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            ACTIVO,
            "Release T.0",
            "Configuración institucional",
            "Español",
            (
                "Perfiles de usuario configurables, alarmas visuales y "
                "audibles configurables, tendencias de hasta 120 horas, "
                "registro automático de eventos y pantallas personalizables."
            ),
        ),
    )

    # INFORMACIÓN REGULATORIA
    cursor.execute(
        """
        INSERT INTO informacion_regulatoria (
            activo,
            registro_sanitario,
            fda,
            norma,
            clasificacion_riesgo
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            ACTIVO,
            "Marcado CE disponible",
            "Conforme a documentación FDA del fabricante",
            "IEC 60601-1 / IEC 60601-1-2",
            "Clase IIb",
        ),
    )

    # MANTENIMIENTOS
    mantenimientos = [
        (
            "2022-09-20",
            "Preventivo",
            "Tec. Mauricio Castro",
            "Limpieza y pruebas funcionales.",
            "No aplica",
            "2023-03-14",
        ),
        (
            "2023-03-14",
            "Preventivo",
            "Tec. Laura Herrera",
            "Verificación de batería y alarmas.",
            "No aplica",
            "2023-10-18",
        ),
        (
            "2023-10-18",
            "Correctivo",
            "Ing. Kevin Sandoval",
            "Cambio de batería interna.",
            "Batería interna",
            "2024-04-27",
        ),
        (
            "2024-04-27",
            "Preventivo",
            "Tec. Daniel Ureña",
            "Inspección eléctrica general.",
            "No aplica",
            "2024-11-11",
        ),
        (
            "2024-11-11",
            "Preventivo",
            "Tec. Valeria Rojas",
            "Revisión de módulos y sensores.",
            "No aplica",
            "2025-05-21",
        ),
        (
            "2025-05-21",
            "Correctivo",
            "Ing. Cristian Solís",
            "Sustitución del módulo NIBP.",
            "Módulo NIBP",
            "2025-10-08",
        ),
        (
            "2025-10-08",
            "Preventivo",
            "Tec. Gabriel Mora",
            "Pruebas de funcionamiento.",
            "No aplica",
            "2026-03-19",
        ),
        (
            "2026-03-19",
            "Preventivo",
            "Tec. Paola Navarro",
            "Verificación de parámetros.",
            "No aplica",
            "2026-07-02",
        ),
        (
            "2026-07-02",
            "Preventivo",
            "Ing. Andrés Vargas",
            "Actualización de software y revisión general.",
            "No aplica",
            "2026-10-10",
        ),
    ]

    for mantenimiento in mantenimientos:
        cursor.execute(
            """
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
            """,
            (ACTIVO, *mantenimiento),
        )

    # CALIBRACIONES
    calibraciones = [
        (
            "2022-09-06",
            "Conforme",
            "CAL-MON-2022-024",
            "Simulador de paciente multiparámetro",
            "2023-09-06",
        ),
        (
            "2023-09-08",
            "Conforme",
            "CAL-MON-2023-036",
            "Simulador ECG, SpO₂ y presión no invasiva",
            "2024-09-08",
        ),
        (
            "2024-09-10",
            "Conforme",
            "CAL-MON-2024-048",
            "Simulador multiparámetro y analizador de seguridad eléctrica",
            "2025-09-10",
        ),
        (
            "2025-09-12",
            "Conforme",
            "CAL-MON-2025-057",
            "Simulador ECG, respiración, SpO₂, NIBP y temperatura",
            "2026-09-12",
        ),
    ]

    for calibracion in calibraciones:
        cursor.execute(
            """
            INSERT INTO calibraciones (
                activo,
                fecha,
                resultado,
                certificado,
                patron_utilizado,
                proxima_calibracion
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ACTIVO, *calibracion),
        )

    # FALLAS
    fallas = [
        (
            "2023-10-17",
            "La batería presenta autonomía reducida.",
            "Batería interna con pérdida de capacidad.",
            (
                "Se sustituyó la batería y se realizaron pruebas "
                "de carga, descarga y autonomía."
            ),
            "5 horas",
        ),
        (
            "2025-05-20",
            "El módulo de presión no invasiva no completa la medición.",
            "Falla interna del módulo NIBP.",
            (
                "Se sustituyó el módulo NIBP y se verificó su funcionamiento "
                "con un simulador de presión."
            ),
            "8 horas",
        ),
    ]

    for falla in fallas:
        cursor.execute(
            """
            INSERT INTO fallas (
                activo,
                fecha,
                falla_reportada,
                diagnostico,
                accion_realizada,
                tiempo_fuera_servicio
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (ACTIVO, *falla),
        )

    # INDICADORES
    cursor.execute(
        """
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
        """,
        (
            ACTIVO,
            "99.3 %",
            "14,620 horas",
            7,
            2,
            4,
            "13 horas",
            "7,310 horas",
            "6.5 horas",
            "100 %",
        ),
    )

    # INFORMACIÓN ECONÓMICA
    cursor.execute(
        """
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
        """,
        (
            ACTIVO,
            22450.00,
            "2 años",
            "2024-08-15",
            1680.00,
            1320.00,
            1040.00,
        ),
    )

    # MANUAL
    cursor.execute(
        """
        INSERT INTO documentos (
            activo,
            manual_usuario
        )
        VALUES (?, ?)
        """,
        (
            ACTIVO,
            "/static/manuales/act-001.pdf",
        ),
    )

    # CÓDIGO QR
    cursor.execute(
        """
        INSERT INTO codigo_qr (
            activo,
            codigo_qr
        )
        VALUES (?, ?)
        """,
        (
            ACTIVO,
            "/equipo/ACT-001",
        ),
    )


def verificar_carga(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
        """
        SELECT activo, nombre, marca, modelo, estado
        FROM equipos
        WHERE activo = ?
        """,
        (ACTIVO,),
    )

    equipo = cursor.fetchone()

    if equipo is None:
        raise RuntimeError("El ACT-001 no fue encontrado después de la carga.")

    tablas = (
        "mantenimientos",
        "calibraciones",
        "fallas",
        "indicadores",
        "informacion_economica",
        "documentos",
    )

    cantidades = {}

    for tabla in tablas:
        cursor.execute(
            f'SELECT COUNT(*) FROM "{tabla}" WHERE activo = ?',
            (ACTIVO,),
        )
        cantidades[tabla] = cursor.fetchone()[0]

    print("\n" + "=" * 72)
    print("ACT-001 CARGADO CORRECTAMENTE")
    print("=" * 72)
    print(f"Activo: {equipo[0]}")
    print(f"Equipo: {equipo[1]}")
    print(f"Marca y modelo: {equipo[2]} {equipo[3]}")
    print(f"Estado: {equipo[4]}")
    print(f"Mantenimientos: {cantidades['mantenimientos']}")
    print(f"Calibraciones: {cantidades['calibraciones']}")
    print(f"Fallas: {cantidades['fallas']}")
    print(f"Indicadores: {cantidades['indicadores']}")
    print(f"Información económica: {cantidades['informacion_economica']}")
    print(f"Documentos: {cantidades['documentos']}")
    print("=" * 72)


def cargar_act001() -> None:
    if not RUTA_BASE_DATOS.exists():
        print(
            "ERROR: No se encontró la base de datos en:\n"
            f"{RUTA_BASE_DATOS}"
        )
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        eliminar_registros_existentes(cursor)
        insertar_act001(cursor)
        conexion.commit()
        verificar_carga(cursor)

        print("\nLos demás activos no fueron modificados.")

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR DURANTE LA CARGA DEL ACT-001")
        print(error)
        print("No se guardaron los cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_act001()
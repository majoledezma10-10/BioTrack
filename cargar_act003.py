import sqlite3
from pathlib import Path


RUTA_BASE_DATOS = Path("database/biotrack_v2.db")
ACTIVO = "ACT-003"


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


def insertar_act003(cursor: sqlite3.Cursor) -> None:
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
            "QR-ACT003",
            "Electrocardiógrafo",
            "Electrocardiógrafo de 12 derivaciones",
            "GE HealthCare",
            "MAC 2000",
            "MAC2000-24-584163",
            "GE HealthCare",
            "China",
            2022,
            "2022-06-18",
            "2022-07-05",
            "Servicio de Cardiología",
            "Consulta Externa",
            "Jefatura de Cardiología",
            "Operativo",
            "Media",
            "10 años",
            (
                "Equipo en excelente estado de funcionamiento. "
                "Pantalla y sistema de impresión funcionando correctamente."
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
            "5200 mAh",
            "IPX0",
            "5.2 kg",
            "355 × 315 × 90 mm",
        ),
    )

            # PARÁMETROS DEL ELECTROCARDIÓGRAFO
    # Las columnas existentes se utilizan para organizar
    # las funciones específicas del electrocardiógrafo.
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
                "Adquisición ECG automática mediante 10 cables y "
                "12 derivaciones simultáneas, con configuración "
                "programable de derivaciones."
            ),
            "Rango del medidor de frecuencia cardíaca: 30 a 300 lpm.",
            (
                "Interpretación mediante el programa de análisis "
                "Marquette 12SL para pacientes adultos y pediátricos."
            ),
            "No aplica",
            "No aplica",
            "No aplica",
            (
                "Mediciones automáticas de los intervalos PR, QRS y QT/QTc, "
                "con análisis del segmento ST. Frecuencia de muestreo de "
                "500 o 1000 muestras/segundo/canal para análisis y "
                "16000 muestras/segundo/canal para adquisición normal. "
                "Ancho de banda de 0.04 a 150 Hz y rechazo de modo común "
                "mayor a 135 dB con filtro de 50/60 Hz activado."
            ),
            (
                "Modos de operación: ECG de reposo de 12 derivaciones "
                "durante 10 segundos, arritmia, prueba de esfuerzo y análisis RR. "
                "Almacenamiento interno de hasta 200 ECG, exportación a PDF "
                "y conectividad LAN/Wi-Fi."
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
            "4.3",
            "2.1",
            "Español",
            "USB / LAN / Wi-Fi, según configuración",
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
            "Consultar documentación regulatoria vigente",
            "Conforme a documentación del fabricante",
            "IEC 60601-1 / IEC 60601-2-25",
            "Clase II",
        ),
    )

    # MANTENIMIENTOS
    mantenimientos = [
        (
            "2022-12-05",
            "Preventivo",
            "Tec. Pablo Jiménez",
            (
                "Inspección física, limpieza externa e interna, revisión del "
                "cable de paciente, electrodos, teclado y sistema de impresión."
            ),
            "Papel térmico",
            "2023-06-05",
        ),
        (
            "2023-06-07",
            "Preventivo",
            "Ing. Natalia Campos",
            (
                "Verificación de las doce derivaciones, prueba de batería, "
                "impresora, pantalla y seguridad eléctrica."
            ),
            "No aplica",
            "2023-12-07",
        ),
        (
            "2023-12-11",
            "Correctivo",
            "Tec. Pablo Jiménez",
            (
                "Corrección de alimentación irregular del papel y limpieza "
                "del mecanismo de impresión."
            ),
            "Rodillo de arrastre",
            "2024-06-11",
        ),
        (
            "2024-06-13",
            "Preventivo",
            "Ing. Natalia Campos",
            (
                "Prueba funcional completa, verificación de señal ECG, "
                "revisión de batería y comprobación de impresión."
            ),
            "No aplica",
            "2024-12-13",
        ),
        (
            "2024-12-16",
            "Preventivo",
            "Tec. Pablo Jiménez",
            (
                "Limpieza técnica, revisión de conectores, cable de paciente, "
                "teclado, pantalla y sistema de almacenamiento."
            ),
            "No aplica",
            "2025-06-16",
        ),
        (
            "2025-06-18",
            "Preventivo",
            "Ing. Natalia Campos",
            (
                "Verificación de derivaciones, precisión de frecuencia "
                "cardíaca, batería, impresora y seguridad eléctrica."
            ),
            "No aplica",
            "2025-12-18",
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
            "2022-07-06",
            "Conforme",
            "CAL-ECG-2022-031",
            "Simulador de paciente multiparámetro",
            "2023-07-06",
        ),
        (
            "2023-07-10",
            "Conforme",
            "CAL-ECG-2023-044",
            "Simulador ECG de 12 derivaciones",
            "2024-07-10",
        ),
        (
            "2024-07-12",
            "Conforme",
            "CAL-ECG-2024-052",
            "Simulador de paciente y analizador de seguridad eléctrica",
            "2025-07-12",
        ),
        (
            "2025-07-14",
            "Conforme",
            "CAL-ECG-2025-058",
            "Simulador ECG de 12 derivaciones",
            "2026-07-14",
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
            "2023-12-08",
            "Atasco recurrente del papel durante la impresión.",
            "Rodillo de arrastre desgastado.",
            (
                "Se sustituyó el rodillo, se limpió el mecanismo "
                "y se realizaron pruebas de impresión."
            ),
            "4 horas",
        ),
        (
            "2024-04-22",
            "Ruido intermitente en una de las derivaciones.",
            "Conector del cable de paciente con residuos superficiales.",
            (
                "Se realizó limpieza técnica del conector y comprobación "
                "de las doce derivaciones."
            ),
            "2 horas",
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
            "99.2 %",
            "3,460 horas",
            5,
            1,
            4,
            "6 horas",
            "1,730 horas",
            "3 horas",
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
            7850.00,
            "2 años",
            "2024-06-18",
            640.00,
            295.00,
            185.00,
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
            "/static/manuales/act-003.pdf",
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
            "/equipo/ACT-003",
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
        raise RuntimeError("El ACT-003 no fue encontrado después de la carga.")

    tablas = (
        "mantenimientos",
        "calibraciones",
        "fallas",
        "indicadores",
        "informacion_economica",
    )

    cantidades = {}

    for tabla in tablas:
        cursor.execute(
            f'SELECT COUNT(*) FROM "{tabla}" WHERE activo = ?',
            (ACTIVO,),
        )
        cantidades[tabla] = cursor.fetchone()[0]

    print("\n" + "=" * 68)
    print("ACT-003 CARGADO CORRECTAMENTE")
    print("=" * 68)
    print(f"Activo: {equipo[0]}")
    print(f"Equipo: {equipo[1]}")
    print(f"Marca y modelo: {equipo[2]} {equipo[3]}")
    print(f"Estado: {equipo[4]}")
    print(f"Mantenimientos: {cantidades['mantenimientos']}")
    print(f"Calibraciones: {cantidades['calibraciones']}")
    print(f"Fallas: {cantidades['fallas']}")
    print(f"Indicadores: {cantidades['indicadores']}")
    print(f"Información económica: {cantidades['informacion_economica']}")
    print("=" * 68)


def cargar_act003() -> None:
    if not RUTA_BASE_DATOS.exists():
        print(
            "ERROR: No se encontró la base de datos en:\n"
            f"{RUTA_BASE_DATOS.resolve()}"
        )
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        eliminar_registros_existentes(cursor)
        insertar_act003(cursor)
        conexion.commit()
        verificar_carga(cursor)

        print("\nLos demás activos no fueron modificados.")

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR DURANTE LA CARGA DEL ACT-003")
        print(error)
        print("No se guardaron los cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_act003()
from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-006"


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


def insertar_act006(cursor: sqlite3.Cursor) -> None:
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
            "QR-ACT006",
            "Bomba de Infusión",
            "Bomba de infusión volumétrica",
            "Baxter",
            "SIGMA Spectrum 35700BAX2",
            "SS-21-583742",
            "Baxter Healthcare Corporation",
            "Estados Unidos",
            2021,
            "2021-05-18",
            "2021-06-04",
            "Ingeniería Clínica",
            "Taller de Electromedicina",
            "Ingeniería Clínica",
            "Fuera de servicio",
            "Alta",
            "10 años",
            (
                "Equipo fuera de servicio por falla recurrente del sensor "
                "de presión de oclusión. Pendiente de sustitución del módulo "
                "y recalibración."
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
            "100-240 VAC, 50/60 Hz; adaptador Baxter P/N 35727",
            "Módulo de batería recargable de ion-litio",
            "Autonomía aproximada de 8 horas",
            "Protección eléctrica Clase I; IEC 60601-1",
            "1.5 kg",
            (
                "Pantalla LCD gráfica, puerto de comunicación IrDA y "
                "conectividad inalámbrica opcional mediante "
                "Wireless Battery Module"
            ),
        ),
    )

    # PARÁMETROS DE INFUSIÓN
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
            "Velocidad de infusión: 0.5 a 999 mL/h. Precisión: ±5 %.",
            "VTBI: 0.1 a 9,999 mL. KVO disponible.",
            (
                "Bolus manual y programable. Infusión secundaria "
                "Piggyback disponible."
            ),
            (
                "Biblioteca de medicamentos Master Drug Library y sistema "
                "DERS disponibles."
            ),
            (
                "Infusión por dosis, cantidad/tiempo y modo Multi-Step "
                "disponibles."
            ),
            (
                "Cyclic TPN, cambio de velocidad sin detener la infusión, "
                "priming y line flush disponibles."
            ),
            (
                "Sistema Anti-Free Flow y bloqueo de teclado disponibles. "
                "Sensor de presión de oclusión configurable."
            ),
            (
                "Alarmas de aire en línea, oclusión, batería baja, batería "
                "agotada, puerta abierta, fin de infusión, error del sistema "
                "y flujo anormal."
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
            "8.00",
            "Master Drug Library versión 8",
            "Inglés",
            (
                "IrDA y conectividad inalámbrica opcional. "
                "Modo BASIC y modo Drug Library disponibles. "
                "Configuración de alarmas programable."
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
            "IEC 60601-1",
            "Clase IIb",
        ),
    )

    # MANTENIMIENTOS
    mantenimientos = [
        (
            "2021-07-16",
            "Preventivo",
            "Tec. Mauricio Castro",
            "Limpieza y prueba funcional.",
            "No aplica",
            "2022-02-10",
        ),
        (
            "2022-02-10",
            "Preventivo",
            "Tec. Laura Herrera",
            "Verificación de batería y alarmas.",
            "No aplica",
            "2022-09-25",
        ),
        (
            "2022-09-25",
            "Correctivo",
            "Ing. Andrés Solís",
            "Cambio del sensor de aire.",
            "Sensor de aire",
            "2023-04-13",
        ),
        (
            "2023-04-13",
            "Preventivo",
            "Tec. Valeria Rojas",
            "Prueba de precisión del flujo.",
            "No aplica",
            "2023-12-07",
        ),
        (
            "2023-12-07",
            "Preventivo",
            "Tec. Daniel Ureña",
            "Inspección eléctrica general.",
            "No aplica",
            "2024-06-21",
        ),
        (
            "2024-06-21",
            "Correctivo",
            "Ing. Cristian Vargas",
            "Reemplazo del módulo de alimentación.",
            "Módulo de alimentación",
            "2024-11-18",
        ),
        (
            "2024-11-18",
            "Preventivo",
            "Tec. Paola Navarro",
            "Limpieza y revisión de sensores.",
            "No aplica",
            "2025-05-28",
        ),
        (
            "2025-05-28",
            "Preventivo",
            "Tec. Gabriel Mora",
            "Verificación de alarmas y batería.",
            "No aplica",
            "2026-01-14",
        ),
        (
            "2026-01-14",
            "Correctivo en proceso",
            "Ing. Kevin Sandoval",
            (
                "Falla del sensor de oclusión. Pendiente de sustitución "
                "del módulo y recalibración."
            ),
            "Módulo del sensor de oclusión pendiente",
            "Se programará cuando el equipo vuelva a servicio",
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
            "2021-06-07",
            "Conforme",
            "CAL-INF-2021-019",
            "Analizador de bombas de infusión",
            "2022-06-07",
        ),
        (
            "2022-06-10",
            "Conforme",
            "CAL-INF-2022-028",
            "Analizador de flujo y presión de oclusión",
            "2023-06-10",
        ),
        (
            "2023-06-13",
            "Conforme",
            "CAL-INF-2023-037",
            "Analizador de bombas de infusión",
            "2024-06-13",
        ),
        (
            "2024-06-24",
            "Conforme",
            "CAL-INF-2024-049",
            "Analizador de flujo, volumen y presión",
            "2025-06-24",
        ),
        (
            "2025-06-27",
            "Conforme",
            "CAL-INF-2025-056",
            "Analizador de bombas de infusión",
            "2026-06-27",
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
            "2022-09-24",
            "Alarma de aire en línea sin presencia visible de burbujas.",
            "Sensor de aire con funcionamiento inestable.",
            (
                "Se sustituyó el sensor de aire y se realizaron "
                "pruebas funcionales."
            ),
            "6 horas",
        ),
        (
            "2024-06-20",
            "El equipo no mantiene la alimentación eléctrica correctamente.",
            "Falla del módulo interno de alimentación.",
            (
                "Se sustituyó el módulo de alimentación y se verificó "
                "el funcionamiento con corriente alterna y batería."
            ),
            "12 horas",
        ),
        (
            "2026-01-13",
            (
                "Alarma recurrente de oclusión sin obstrucción en "
                "la línea de infusión."
            ),
            (
                "Falla del sensor de presión de oclusión. El módulo "
                "requiere sustitución y recalibración."
            ),
            (
                "Equipo retirado del servicio y trasladado al Taller de "
                "Electromedicina. Repuesto pendiente."
            ),
            "Fuera de servicio desde 2026-01-14",
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
            "82.4 %",
            "10,850 horas",
            6,
            3,
            5,
            "Fuera de servicio desde 2026-01-14",
            "3,617 horas",
            "Pendiente de reparación",
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
            7250.00,
            "2 años",
            "2023-05-18",
            1120.00,
            1780.00,
            1460.00,
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
            "/static/manuales/act-006.pdf",
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
            "/equipo/ACT-006",
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
        raise RuntimeError("El ACT-006 no fue encontrado después de la carga.")

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
    print("ACT-006 CARGADO CORRECTAMENTE")
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


def cargar_act006() -> None:
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
        insertar_act006(cursor)
        conexion.commit()
        verificar_carga(cursor)

        print("\nLos demás activos no fueron modificados.")

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR DURANTE LA CARGA DEL ACT-006")
        print(error)
        print("No se guardaron los cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_act006()
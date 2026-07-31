from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-004"


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


def insertar_act004(cursor: sqlite3.Cursor) -> None:
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
            "QR-ACT004",
            "Bomba de infusión",
            "Bomba de infusión volumétrica",
            "Baxter",
            "Sigma Spectrum",
            "SS-22-845193",
            "Baxter Healthcare Corporation",
            "Estados Unidos",
            2022,
            "2022-05-10",
            "2022-05-27",
            "Servicio de Hospitalización",
            "Medicina Interna",
            "Coordinación de Enfermería",
            "Operativo",
            "Alta",
            "10 años",
            (
                "Equipo en óptimas condiciones de funcionamiento. "
                "Se encuentra integrado al sistema de gestión de bombas "
                "de infusión del hospital."
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
            "7.2 V, 1800 mAh; autonomía aproximada de 8 horas a 125 mL/h",
            "IPX1",
            "0.95 kg con abrazadera para poste",
            "14.7 × 16.3 × 11.9 cm",
        ),
    )

    # PARÁMETROS DE INFUSIÓN
    # Se adaptan a las columnas disponibles en la tabla actual.
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
                "Velocidad de infusión: 0.5-1.9 mL/h con precisión de ±0.1 mL/h; "
                "2.0-999 mL/h con precisión de ±5 %."
            ),
            "VTBI: 0.01-9,999 mL.",
            (
                "Presión de oclusión ajustable: baja 8 ±4 PSI; "
                "media 13 ±8 PSI; alta 18 ±9 PSI; "
                "presión máxima desarrollada 38 PSI."
            ),
            (
                "KVO disponible: mantiene una velocidad de 1 mL/h "
                "o la velocidad programada, la que sea menor."
            ),
            (
                "Detección de aire en línea: burbujas de aproximadamente "
                "140 µL y alarma por acumulación superior a 1 mL "
                "en un período de 15 minutos."
            ),
            (
                "Biblioteca de medicamentos disponible. "
                "Límite blando permite continuar tras confirmación; "
                "límite duro impide iniciar la infusión fuera del rango permitido."
            ),
            (
                "Registro de eventos independiente para la bomba y para "
                "la biblioteca de medicamentos, con al menos 8 horas "
                "de eventos o registro completo."
            ),
            (
                "Infusión secundaria disponible. La velocidad máxima depende "
                "del equipo de administración utilizado. Alarmas: aire en línea, "
                "fin de infusión, puerta abierta, inactividad de 2 minutos "
                "y error del sistema."
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
            "8.0",
            "Español",
            "USB / Infrarrojo / Wi-Fi, según módulo instalado",
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
            "Conforme a la documentación del fabricante",
            "IEC 60601-1 / IEC 60601-2-24",
            "Clase IIb",
        ),
    )

       # HISTORIAL DE MANTENIMIENTO
    mantenimientos = [
        (
            "2022-08-18",
            "Preventivo",
            "Tec. Mauricio Castro",
            "Limpieza general, inspección visual y pruebas funcionales.",
            "No aplica",
            "2023-02-23",
        ),
        (
            "2023-02-23",
            "Preventivo",
            "Tec. Paola Navarro",
            "Verificación de batería, alarmas y precisión de infusión.",
            "No aplica",
            "2023-10-12",
        ),
        (
            "2023-10-12",
            "Correctivo",
            "Ing. Kevin Sandoval",
            "Reemplazo de batería interna y prueba de funcionamiento.",
            "Batería interna",
            "2024-03-21",
        ),
        (
            "2024-03-21",
            "Preventivo",
            "Tec. Roxana Murillo",
            "Limpieza, revisión de sensores y comprobación del flujo.",
            "No aplica",
            "2024-09-05",
        ),
        (
            "2024-09-05",
            "Preventivo",
            "Tec. Alejandro Gamboa",
            "Inspección eléctrica y verificación de alarmas.",
            "No aplica",
            "2025-01-16",
        ),
        (
            "2025-01-16",
            "Correctivo",
            "Ing. Esteban Vargas",
            "Sustitución del sensor de aire en línea y pruebas funcionales.",
            "Sensor de aire en línea",
            "2025-05-28",
        ),
        (
            "2025-05-28",
            "Preventivo",
            "Tec. Laura Céspedes",
            "Limpieza, revisión mecánica y prueba de batería.",
            "No aplica",
            "2025-11-18",
        ),
        (
            "2025-11-18",
            "Preventivo",
            "Tec. Daniel Ureña",
            "Verificación de la biblioteca de medicamentos y flujo de infusión.",
            "No aplica",
            "2026-03-09",
        ),
        (
            "2026-03-09",
            "Preventivo",
            "Tec. Valeria Alvarado",
            "Revisión general y comprobación de parámetros de infusión.",
            "No aplica",
            "2026-06-24",
        ),
        (
            "2026-06-24",
            "Preventivo",
            "Ing. Cristian Solís",
            "Calibración, actualización de software y pruebas finales.",
            "No aplica",
            "2026-12-24",
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
            "2022-05-30",
            "Conforme",
            "CAL-INF-2022-021",
            "Analizador de bombas de infusión",
            "2023-05-30",
        ),
        (
            "2023-06-02",
            "Conforme",
            "CAL-INF-2023-034",
            "Analizador de flujo y volumen",
            "2024-06-02",
        ),
        (
            "2024-06-05",
            "Conforme",
            "CAL-INF-2024-046",
            "Analizador de bombas de infusión y seguridad eléctrica",
            "2025-06-05",
        ),
        (
            "2025-06-09",
            "Conforme",
            "CAL-INF-2025-053",
            "Analizador de flujo, volumen y presión de oclusión",
            "2026-06-09",
        ),
        (
            "2026-06-12",
            "Conforme",
            "CAL-INF-2026-061",
            "Analizador de bombas de infusión",
            "2027-06-12",
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
            "2023-10-10",
            "La batería presenta una autonomía inferior a la esperada.",
            "Batería interna con pérdida de capacidad.",
            (
                "Se sustituyó la batería y se realizaron pruebas de carga, "
                "descarga y funcionamiento."
            ),
            "5 horas",
        ),
        (
            "2025-01-15",
            "Alarma intermitente del detector de aire en línea.",
            "Sensor de aire en línea con respuesta inestable.",
            (
                "Se sustituyó el sensor y se verificó el funcionamiento "
                "mediante pruebas técnicas."
            ),
            "7 horas",
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
            "99.4 %",
            "8,760 horas",
            8,
            2,
            5,
            "12 horas",
            "4,380 horas",
            "6 horas",
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
            6950.00,
            "2 años",
            "2024-05-10",
            980.00,
            525.00,
            390.00,
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
            "/static/manuales/act-004.pdf",
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
            "/equipo/ACT-004",
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
        raise RuntimeError("El ACT-004 no fue encontrado después de la carga.")

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

    print("\n" + "=" * 68)
    print("ACT-004 CARGADO CORRECTAMENTE")
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
    print(f"Documentos: {cantidades['documentos']}")
    print("=" * 68)


def cargar_act004() -> None:
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
        insertar_act004(cursor)
        conexion.commit()
        verificar_carga(cursor)

        print("\nLos demás activos no fueron modificados.")

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR DURANTE LA CARGA DEL ACT-004")
        print(error)
        print("No se guardaron los cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_act004()
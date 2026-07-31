from pathlib import Path
import sqlite3


CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"
ACTIVO = "ACT-005"


def eliminar_registros_existentes(cursor: sqlite3.Cursor) -> None:
    """Elimina solamente la información anterior del ACT-005."""

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


def insertar_act005(cursor: sqlite3.Cursor) -> None:
    """Inserta toda la información correspondiente al ACT-005."""

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
            "QR-ACT005",
            "Ventilador mecánico",
            "Ventilador mecánico de cuidados intensivos",
            "Dräger",
            "Savina 300",
            "SAV300-22-761845",
            "Dräger Medical GmbH",
            "Alemania",
            2021,
            "2021-09-14",
            "2021-10-04",
            "Unidad de Cuidados Intensivos (UCI)",
            "Terapia Respiratoria",
            "Coordinación de Terapia Respiratoria",
            "En pausa por mantenimiento correctivo",
            "Alta",
            "10 años",
            (
                "Equipo fuera de servicio temporalmente por falla en el módulo "
                "de suministro de aire. Pendiente de instalación del repuesto "
                "y pruebas funcionales antes de volver a operación."
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
            "Autonomía aproximada de 45 minutos",
            "IP21",
            "26 kg",
            "590 × 390 × 490 mm",
        ),
    )

      # PARÁMETROS MONITORIZADOS
    # Las columnas existentes se reutilizan para organizar
    # los parámetros respiratorios del ventilador.
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
                "Presiones de vía aérea: presión pico (PIP), presión meseta, "
                "presión media y PEEP, con rango de 0 a 99 mbar o cmH₂O."
            ),
            (
                "Volumen corriente inspirado, espirado y espontáneo: "
                "0 a 3999 mL BTPS. Volumen minuto total y espontáneo: "
                "0 a 99 L/min."
            ),
            (
                "Frecuencia respiratoria total y espontánea: "
                "0 a 150 respiraciones por minuto."
            ),
            (
                "FiO₂: 21 a 100 % Vol. Relación I:E: "
                "1:150 hasta 150:1."
            ),
            (
                "PEEP y PEEP intermitente ajustables: "
                "0 a 50 mbar, hPa o cmH₂O."
            ),
            (
                "Compliancia dinámica: 0.5 a 200 mL/mbar o mL/cmH₂O. "
                "Resistencia de la vía aérea disponible como valor calculado."
            ),
            (
                "Curvas disponibles: Paw(t), flujo(t), volumen corriente(t) "
                "y CO₂(t). Loops respiratorios y tendencias disponibles."
            ),
            (
                "EtCO₂ mediante módulo opcional: 0 a 100 mmHg. "
                "Modos de ventilación: VC-CMV/VC-AC, VC-SIMV, VC-MMV, "
                "PC-BIPAP, PC-AC, PC-APRV y SPN-CPAP. "
                "NIV y oxigenoterapia disponibles de forma opcional."
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
            "5.0",
            "5.2",
            "Español",
            "Ethernet / USB",
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
            "Vigente",
            "Conforme a la documentación del fabricante; marcado CE disponible",
            "IEC 60601-1 / IEC 60601-2-12",
            "Clase IIb",
        ),
    )

    # HISTORIAL DE MANTENIMIENTOS
    mantenimientos = [
        (
            "2022-04-08",
            "Preventivo",
            "Tec. Carlos Hernández",
            (
                "Limpieza técnica, inspección de conexiones neumáticas, "
                "prueba de batería, pantalla, alarmas y funcionamiento general."
            ),
            "Filtro de entrada de aire",
            "2022-10-08",
        ),
        (
            "2022-10-14",
            "Preventivo",
            "Ing. Adriana Salas",
            (
                "Verificación de volumen, presión, frecuencia respiratoria, "
                "PEEP, FiO₂ y seguridad eléctrica."
            ),
            "No aplica",
            "2023-04-14",
        ),
        (
            "2023-04-18",
            "Preventivo",
            "Tec. Luis Ramírez",
            (
                "Revisión del circuito neumático, sensores, válvulas, "
                "turbina, batería interna y sistema de alarmas."
            ),
            "Filtro de polvo",
            "2023-10-18",
        ),
        (
            "2023-10-20",
            "Correctivo",
            "Ing. Andrea Mora",
            (
                "Corrección de alarma de batería y sustitución del acumulador "
                "interno. Se realizaron pruebas de autonomía."
            ),
            "Batería interna",
            "2024-04-20",
        ),
        (
            "2024-04-25",
            "Preventivo",
            "Tec. Roberto Chaves",
            (
                "Limpieza interna, verificación de turbina, presión, volumen, "
                "flujo, FiO₂, PEEP y alarmas."
            ),
            "Filtro bacteriano",
            "2024-10-25",
        ),
        (
            "2024-10-29",
            "Preventivo",
            "Ing. Natalia Campos",
            (
                "Prueba funcional completa, comprobación de modos ventilatorios "
                "y verificación de seguridad eléctrica."
            ),
            "No aplica",
            "2025-04-29",
        ),
        (
            "2025-05-02",
            "Preventivo",
            "Tec. Pablo Jiménez",
            (
                "Revisión de sensores de presión y flujo, circuito neumático, "
                "batería, pantalla y alarmas."
            ),
            "Filtro de entrada",
            "2025-11-02",
        ),
        (
            "2025-11-07",
            "Preventivo",
            "Ing. Daniela Vargas",
            (
                "Mantenimiento preventivo general y comprobación de precisión "
                "en volumen, presión, frecuencia, PEEP y FiO₂."
            ),
            "No aplica",
            "2026-05-07",
        ),
        (
            "2026-05-12",
            "Preventivo",
            "Tec. Andrés Solano",
            (
                "Inspección preventiva, limpieza técnica y detección de "
                "respuesta irregular en el módulo de suministro de aire."
            ),
            "No aplica",
            "2026-11-12",
        ),
        (
            "2026-07-22",
            "Correctivo en proceso",
            "Ing. Natalia Campos",
            (
                "Diagnóstico de falla en el módulo de suministro de aire. "
                "Equipo retirado temporalmente del servicio y pendiente de "
                "instalación del repuesto."
            ),
            "Módulo de suministro de aire pendiente",
            "Pendiente de finalizar reparación",
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
            "2021-10-05",
            "Conforme",
            "CAL-VENT-2021-018",
            "Analizador de ventiladores y analizador de seguridad eléctrica",
            "2022-10-05",
        ),
        (
            "2022-10-10",
            "Conforme",
            "CAL-VENT-2022-029",
            "Analizador de flujo, volumen, presión y concentración de oxígeno",
            "2023-10-10",
        ),
        (
            "2023-10-16",
            "Conforme",
            "CAL-VENT-2023-041",
            "Analizador de ventiladores pulmonares",
            "2024-10-16",
        ),
        (
            "2024-10-21",
            "Conforme",
            "CAL-VENT-2024-054",
            "Analizador de flujo, presión, volumen y FiO₂",
            "2025-10-21",
        ),
        (
            "2025-10-24",
            "Conforme",
            "CAL-VENT-2025-067",
            "Analizador de ventiladores y pulmón de prueba",
            "2026-10-24",
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
            "2023-10-18",
            "Alarma de batería y autonomía reducida.",
            "Batería interna con pérdida de capacidad.",
            (
                "Se sustituyó la batería y se verificaron la carga, "
                "la autonomía y el funcionamiento con alimentación eléctrica."
            ),
            "8 horas",
        ),
        (
            "2026-07-21",
            (
                "Alarma de suministro de aire y funcionamiento irregular "
                "durante la prueba de inicio."
            ),
            (
                "Falla confirmada en el módulo interno de suministro de aire. "
                "El equipo no debe utilizarse clínicamente hasta completar "
                "la reparación."
            ),
            (
                "Equipo retirado del servicio. Se solicitó el repuesto y el "
                "mantenimiento correctivo permanece abierto."
            ),
            "En mantenimiento",
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
            "96.8 %",
            "18,420 horas",
            8,
            2,
            5,
            "Equipo actualmente en mantenimiento",
            "9,210 horas",
            "Pendiente de cierre del mantenimiento actual",
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
            28750.00,
            "2 años",
            "2023-09-14",
            2850.00,
            1960.00,
            1640.00,
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
            "/static/manuales/act-005.pdf",
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
            "/equipo/ACT-005",
        ),
    )


def verificar_carga(cursor: sqlite3.Cursor) -> None:
    """Comprueba que todas las secciones hayan sido cargadas."""

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
        raise RuntimeError("El ACT-005 no fue encontrado después de la carga.")

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
    print("ACT-005 CARGADO CORRECTAMENTE")
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


def cargar_act005() -> None:
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
        insertar_act005(cursor)
        conexion.commit()
        verificar_carga(cursor)

        print("\nLos demás activos no fueron modificados.")

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print("\nERROR DURANTE LA CARGA DEL ACT-005")
        print(error)
        print("No se guardaron los cambios.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_act005()
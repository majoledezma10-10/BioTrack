import sqlite3
from pathlib import Path


RUTA_BASE_DATOS = Path("database/biotrack_v2.db")

ACTIVOS_NUEVOS = (
    "ACT-002",
    "ACT-003",
    "ACT-004",
    "ACT-005",
    "ACT-006",
)


EQUIPOS = [
    {
        "equipo": (
            "ACT-002",
            "/equipo/ACT-002",
            "Desfibrilador",
            "Desfibrilador externo con monitor",
            "Philips",
            "HeartStart XL+",
            "XL2023-58421",
            "Philips Medical Systems",
            "Estados Unidos",
            2023,
            "2023-04-18",
            "2023-05-03",
            "Servicio de Emergencias",
            "Emergencias",
            "Coordinación de Emergencias",
            "Operativo",
            "Alta",
            "10 años",
            "Equipo destinado a reanimación y monitoreo durante emergencias. "
            "Datos simulados con fines académicos.",
        ),
        "tecnica": (
            "100-240 V AC, 50/60 Hz",
            "Ion-litio recargable",
            "Aproximadamente 3 horas de monitoreo continuo",
            "IP21",
            "6.8 kg aproximadamente",
            "29.6 × 23.1 × 27.9 cm",
        ),
        "parametros": (
            "Disponible, 3 y 5 derivaciones",
            "30-300 lpm",
            "Disponible mediante ECG",
            "Disponible mediante módulo compatible",
            "Disponible",
            "Disponible",
            "No aplica",
            "Disponible mediante módulo opcional",
        ),
        "configuracion": (
            "Versión académica simulada 3.2",
            "Firmware simulado 2.8",
            "Español",
            "USB, red hospitalaria y exportación de eventos",
        ),
        "regulatoria": (
            "Registro simulado para proyecto académico",
            "Dispositivo de referencia comercial autorizado",
            "IEC 60601-1 / IEC 60601-2-4",
            "Clase de riesgo alta",
        ),
        "mantenimientos": [
            (
                "2023-08-10",
                "Preventivo",
                "Ing. Laura Méndez",
                "Inspección física, limpieza interna, revisión de batería, "
                "cables, palas y prueba funcional.",
                "No aplica",
                "2024-02-10",
            ),
            (
                "2024-02-12",
                "Preventivo",
                "Tec. Daniel Vargas",
                "Verificación de descarga, prueba del modo monitor y revisión "
                "de accesorios.",
                "Electrodos de prueba",
                "2024-08-12",
            ),
            (
                "2024-08-14",
                "Correctivo",
                "Ing. Laura Méndez",
                "Corrección de falso contacto en el cable de ECG.",
                "Cable ECG de reemplazo",
                "2025-02-14",
            ),
            (
                "2025-02-17",
                "Preventivo",
                "Tec. Andrea Solano",
                "Prueba de energía entregada, revisión de alarmas y autonomía.",
                "No aplica",
                "2025-08-17",
            ),
        ],
        "calibraciones": [
            (
                "2023-05-04",
                "Conforme",
                "CAL-DF-2023-018",
                "Analizador de desfibriladores",
                "2024-05-04",
            ),
            (
                "2024-05-06",
                "Conforme",
                "CAL-DF-2024-026",
                "Analizador de desfibriladores y simulador ECG",
                "2025-05-06",
            ),
            (
                "2025-05-08",
                "Conforme",
                "CAL-DF-2025-031",
                "Analizador de desfibriladores",
                "2026-05-08",
            ),
        ],
        "fallas": [
            (
                "2024-08-13",
                "Señal ECG intermitente.",
                "Cable de paciente con falso contacto.",
                "Se sustituyó el cable y se realizaron pruebas funcionales.",
                "5 horas",
            ),
            (
                "2025-01-21",
                "Autonomía de batería menor a la esperada.",
                "Batería con degradación moderada.",
                "Se realizó ciclo de acondicionamiento y seguimiento.",
                "2 horas",
            ),
        ],
        "indicadores": (
            "98.6 %",
            "2,340 horas",
            3,
            1,
            3,
            "7 horas",
            "780 horas",
            "3.5 horas",
            "100 %",
        ),
        "economica": (
            18500.00,
            "2 años",
            "2025-04-18",
            980.00,
            620.00,
            410.00,
        ),
    },
    {
        "equipo": (
            "ACT-003",
            "/equipo/ACT-003",
            "Bomba de Infusión",
            "Bomba de infusión volumétrica",
            "Baxter",
            "Sigma Spectrum",
            "BS230154",
            "Baxter Healthcare",
            "Estados Unidos",
            2023,
            "2023-06-12",
            "2023-06-27",
            "UCI Adultos",
            "Cuidados Intensivos",
            "Jefatura de Enfermería UCI",
            "Operativo",
            "Alta",
            "8 años",
            "Bomba destinada a la administración controlada de medicamentos. "
            "Datos simulados con fines académicos.",
        ),
        "tecnica": (
            "100-240 V AC, 50/60 Hz",
            "Ion-litio recargable",
            "Hasta 8 horas según condiciones de uso",
            "IPX2",
            "4.5 kg aproximadamente",
            "21 × 15 × 23 cm",
        ),
        "parametros": (
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
        ),
        "configuracion": (
            "Biblioteca de medicamentos simulada 5.1",
            "Firmware simulado 8.4",
            "Español",
            "Ethernet, Wi-Fi y biblioteca de fármacos",
        ),
        "regulatoria": (
            "Registro simulado para proyecto académico",
            "Dispositivo de referencia comercial autorizado",
            "IEC 60601-1 / IEC 60601-2-24",
            "Clase II",
        ),
        "mantenimientos": [
            (
                "2023-09-05",
                "Preventivo",
                "Tec. Marco Ruiz",
                "Limpieza, revisión del mecanismo de bombeo y prueba de alarmas.",
                "No aplica",
                "2024-03-05",
            ),
            (
                "2024-03-07",
                "Preventivo",
                "Ing. Sofía Araya",
                "Prueba de flujo, oclusión, puerta y sensor de aire.",
                "No aplica",
                "2024-09-07",
            ),
            (
                "2024-09-09",
                "Correctivo",
                "Tec. Marco Ruiz",
                "Ajuste del sensor de cierre de puerta.",
                "Microinterruptor",
                "2025-03-09",
            ),
            (
                "2025-03-11",
                "Preventivo",
                "Ing. Sofía Araya",
                "Verificación de flujo, batería y alarmas audibles.",
                "No aplica",
                "2025-09-11",
            ),
        ],
        "calibraciones": [
            (
                "2023-06-28",
                "Conforme",
                "CAL-BI-2023-041",
                "Analizador de bombas de infusión",
                "2024-06-28",
            ),
            (
                "2024-07-01",
                "Conforme",
                "CAL-BI-2024-049",
                "Analizador de flujo y presión",
                "2025-07-01",
            ),
        ],
        "fallas": [
            (
                "2024-09-08",
                "La puerta no era reconocida correctamente.",
                "Microinterruptor desajustado.",
                "Se ajustó y posteriormente se sustituyó el componente.",
                "6 horas",
            ),
            (
                "2025-02-03",
                "Alarma de oclusión sensible.",
                "Configuración alterada después de limpieza.",
                "Se restablecieron parámetros y se verificó el flujo.",
                "1 hora",
            ),
        ],
        "indicadores": (
            "98.9 %",
            "4,180 horas",
            3,
            1,
            2,
            "7 horas",
            "1,045 horas",
            "3.5 horas",
            "100 %",
        ),
        "economica": (
            4650.00,
            "2 años",
            "2025-06-12",
            420.00,
            310.00,
            185.00,
        ),
    },
    {
        "equipo": (
            "ACT-004",
            "/equipo/ACT-004",
            "Ventilador Mecánico",
            "Ventilador para cuidados intensivos",
            "Dräger",
            "Savina 300",
            "SV300-22418",
            "Drägerwerk AG & Co.",
            "Alemania",
            2022,
            "2022-11-08",
            "2022-11-22",
            "UCI Adultos",
            "Cuidados Intensivos",
            "Coordinación de Terapia Respiratoria",
            "En mantenimiento",
            "Alta",
            "10 años",
            "Equipo actualmente en mantenimiento preventivo programado. "
            "Datos simulados con fines académicos.",
        ),
        "tecnica": (
            "100-240 V AC, 50/60 Hz",
            "Batería interna recargable",
            "Aproximadamente 45 minutos",
            "IP21",
            "26 kg aproximadamente",
            "57.7 × 129.5 × 67.7 cm con carro",
        ),
        "parametros": (
            "No aplica",
            "No aplica",
            "Frecuencia respiratoria monitorizada",
            "SpO₂ mediante módulo opcional",
            "No aplica",
            "Temperatura interna del sistema",
            "Presiones inspiratoria y espiratoria",
            "EtCO₂ mediante módulo opcional",
        ),
        "configuracion": (
            "Software simulado 5.0",
            "Firmware simulado 4.6",
            "Español",
            "Puerto de servicio, red y exportación de tendencias",
        ),
        "regulatoria": (
            "Registro simulado para proyecto académico",
            "Dispositivo de referencia comercial autorizado",
            "IEC 60601-1 / IEC 60601-2-12",
            "Clase de riesgo alta",
        ),
        "mantenimientos": [
            (
                "2023-05-18",
                "Preventivo",
                "Ing. Carlos Quesada",
                "Limpieza interna, revisión de filtros y prueba del circuito.",
                "Filtro de aire",
                "2023-11-18",
            ),
            (
                "2023-11-20",
                "Preventivo",
                "Tec. Melissa Rojas",
                "Verificación de presión, volumen y alarmas.",
                "No aplica",
                "2024-05-20",
            ),
            (
                "2024-05-22",
                "Correctivo",
                "Ing. Carlos Quesada",
                "Corrección de lectura irregular del sensor de presión.",
                "Sensor de presión",
                "2024-11-22",
            ),
            (
                "2024-11-25",
                "Preventivo",
                "Tec. Melissa Rojas",
                "Revisión del sistema neumático y prueba eléctrica.",
                "Filtro bacteriano",
                "2025-05-25",
            ),
            (
                "2025-05-26",
                "Preventivo en proceso",
                "Ing. Carlos Quesada",
                "Mantenimiento programado con verificación de turbina, "
                "válvulas, batería y alarmas.",
                "Kit de filtros",
                "Pendiente de finalizar",
            ),
        ],
        "calibraciones": [
            (
                "2022-11-23",
                "Conforme",
                "CAL-VM-2022-014",
                "Analizador de ventiladores",
                "2023-11-23",
            ),
            (
                "2023-11-24",
                "Conforme",
                "CAL-VM-2023-033",
                "Analizador de flujo, presión y volumen",
                "2024-11-24",
            ),
            (
                "2024-11-26",
                "Conforme",
                "CAL-VM-2024-038",
                "Analizador de ventiladores",
                "2025-11-26",
            ),
        ],
        "fallas": [
            (
                "2024-05-21",
                "Lectura inestable de presión inspiratoria.",
                "Sensor de presión con desviación.",
                "Se reemplazó el sensor y se verificó el sistema.",
                "18 horas",
            ),
            (
                "2025-05-25",
                "Aviso de mantenimiento programado.",
                "Horas de uso alcanzaron el límite preventivo.",
                "Equipo retirado temporalmente para mantenimiento.",
                "En proceso",
            ),
        ],
        "indicadores": (
            "94.2 %",
            "6,820 horas",
            4,
            1,
            3,
            "Actualmente en mantenimiento",
            "1,364 horas",
            "18 horas",
            "100 %",
        ),
        "economica": (
            29800.00,
            "2 años",
            "2024-11-08",
            1450.00,
            1780.00,
            1250.00,
        ),
    },
    {
        "equipo": (
            "ACT-005",
            "/equipo/ACT-005",
            "Electrocardiógrafo",
            "Electrocardiógrafo de 12 derivaciones",
            "GE Healthcare",
            "MAC 2000",
            "GE-MAC2-75830",
            "GE Healthcare",
            "Estados Unidos",
            2021,
            "2021-09-15",
            "2021-10-01",
            "Consulta Externa",
            "Cardiología",
            "Coordinación de Cardiología",
            "Operativo",
            "Media",
            "10 años",
            "Equipo utilizado para estudios electrocardiográficos de reposo. "
            "Datos simulados con fines académicos.",
        ),
        "tecnica": (
            "100-240 V AC, 50/60 Hz",
            "Batería recargable",
            "Hasta 3 horas de uso típico",
            "IP20",
            "6.2 kg aproximadamente",
            "39 × 33 × 15 cm",
        ),
        "parametros": (
            "12 derivaciones",
            "30-300 lpm",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
        ),
        "configuracion": (
            "Software simulado 1.7",
            "Firmware simulado 2.2",
            "Español",
            "USB, red y exportación PDF",
        ),
        "regulatoria": (
            "Registro simulado para proyecto académico",
            "Dispositivo de referencia comercial autorizado",
            "IEC 60601-1 / IEC 60601-2-25",
            "Clase II",
        ),
        "mantenimientos": [
            (
                "2022-04-04",
                "Preventivo",
                "Tec. Pablo Jiménez",
                "Limpieza, revisión de cable de paciente e impresora.",
                "Papel térmico",
                "2022-10-04",
            ),
            (
                "2022-10-06",
                "Correctivo",
                "Ing. Natalia Campos",
                "Corrección de atasco frecuente en impresora.",
                "Rodillo de arrastre",
                "2023-04-06",
            ),
            (
                "2023-04-10",
                "Preventivo",
                "Tec. Pablo Jiménez",
                "Prueba de derivaciones, batería y sistema de impresión.",
                "No aplica",
                "2023-10-10",
            ),
            (
                "2023-10-12",
                "Preventivo",
                "Ing. Natalia Campos",
                "Verificación de señal y seguridad eléctrica.",
                "No aplica",
                "2024-04-12",
            ),
            (
                "2024-04-15",
                "Preventivo",
                "Tec. Pablo Jiménez",
                "Limpieza interna y revisión de accesorios.",
                "Cable de alimentación",
                "2024-10-15",
            ),
            (
                "2024-10-17",
                "Preventivo",
                "Ing. Natalia Campos",
                "Prueba funcional completa y revisión de batería.",
                "No aplica",
                "2025-04-17",
            ),
            (
                "2025-04-21",
                "Preventivo",
                "Tec. Pablo Jiménez",
                "Revisión de señal ECG, teclado e impresora.",
                "No aplica",
                "2025-10-21",
            ),
        ],
        "calibraciones": [
            (
                "2021-10-04",
                "Conforme",
                "CAL-ECG-2021-010",
                "Simulador de paciente",
                "2022-10-04",
            ),
            (
                "2022-10-07",
                "Conforme",
                "CAL-ECG-2022-022",
                "Simulador ECG",
                "2023-10-07",
            ),
            (
                "2023-10-09",
                "Conforme",
                "CAL-ECG-2023-028",
                "Simulador ECG de 12 derivaciones",
                "2024-10-09",
            ),
            (
                "2024-10-11",
                "Conforme",
                "CAL-ECG-2024-034",
                "Simulador de paciente",
                "2025-10-11",
            ),
        ],
        "fallas": [
            (
                "2022-10-05",
                "Atasco recurrente del papel.",
                "Rodillo de arrastre desgastado.",
                "Se sustituyó el rodillo y se limpió el mecanismo.",
                "4 horas",
            ),
            (
                "2024-03-18",
                "Una derivación presentaba ruido.",
                "Conector del cable de paciente contaminado.",
                "Se realizó limpieza técnica y prueba funcional.",
                "2 horas",
            ),
        ],
        "indicadores": (
            "99.1 %",
            "3,120 horas",
            6,
            1,
            4,
            "6 horas",
            "1,560 horas",
            "3 horas",
            "100 %",
        ),
        "economica": (
            7800.00,
            "2 años",
            "2023-09-15",
            540.00,
            430.00,
            260.00,
        ),
    },
    {
        "equipo": (
            "ACT-006",
            "/equipo/ACT-006",
            "Bomba de Infusión",
            "Bomba de infusión volumétrica",
            "Baxter",
            "Sigma Spectrum",
            "BS240811",
            "Baxter Healthcare",
            "Estados Unidos",
            2024,
            "2024-01-22",
            "2024-02-05",
            "Hospitalización",
            "Medicina Interna",
            "Jefatura de Enfermería",
            "Fuera de servicio",
            "Alta",
            "8 años",
            "Equipo retirado por una falla electrónica pendiente de reparación. "
            "Datos simulados con fines académicos.",
        ),
        "tecnica": (
            "100-240 V AC, 50/60 Hz",
            "Ion-litio recargable",
            "Hasta 8 horas según condiciones de uso",
            "IPX2",
            "4.5 kg aproximadamente",
            "21 × 15 × 23 cm",
        ),
        "parametros": (
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
            "No aplica",
        ),
        "configuracion": (
            "Biblioteca de medicamentos simulada 5.1",
            "Firmware simulado 8.4",
            "Español",
            "Ethernet, Wi-Fi y biblioteca de fármacos",
        ),
        "regulatoria": (
            "Registro simulado para proyecto académico",
            "Dispositivo de referencia comercial autorizado",
            "IEC 60601-1 / IEC 60601-2-24",
            "Clase II",
        ),
        "mantenimientos": [
            (
                "2024-05-06",
                "Preventivo",
                "Tec. Marco Ruiz",
                "Limpieza, prueba de flujo, batería y alarmas.",
                "No aplica",
                "2024-11-06",
            ),
            (
                "2024-11-08",
                "Preventivo",
                "Ing. Sofía Araya",
                "Revisión de sistema de bombeo y sensor de aire.",
                "No aplica",
                "2025-05-08",
            ),
            (
                "2025-04-29",
                "Correctivo",
                "Ing. Sofía Araya",
                "Diagnóstico de falla electrónica en la tarjeta principal.",
                "Pendiente: tarjeta principal",
                "Pendiente de reparación",
            ),
        ],
        "calibraciones": [
            (
                "2024-02-06",
                "Conforme",
                "CAL-BI-2024-012",
                "Analizador de bombas de infusión",
                "2025-02-06",
            ),
            (
                "2025-02-07",
                "Conforme",
                "CAL-BI-2025-015",
                "Analizador de flujo y presión",
                "2026-02-07",
            ),
        ],
        "fallas": [
            (
                "2024-08-19",
                "Alarma de aire en línea sin causa aparente.",
                "Sensor con suciedad superficial.",
                "Limpieza especializada y verificación.",
                "3 horas",
            ),
            (
                "2025-04-28",
                "El equipo no completa el encendido.",
                "Falla electrónica en la tarjeta principal.",
                "Equipo retirado de operación; repuesto pendiente.",
                "Fuera de servicio desde 2025-04-28",
            ),
        ],
        "indicadores": (
            "71.4 %",
            "1,980 horas",
            2,
            1,
            2,
            "Fuera de servicio desde 2025-04-28",
            "990 horas",
            "Pendiente de reparación",
            "100 %",
        ),
        "economica": (
            4750.00,
            "2 años",
            "2026-01-22",
            380.00,
            1450.00,
            1250.00,
        ),
    },
]


def eliminar_datos_existentes(cursor, activo):
    tablas_dependientes = [
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
    ]

    for tabla in tablas_dependientes:
        cursor.execute(
            f'DELETE FROM "{tabla}" WHERE activo = ?',
            (activo,),
        )

    cursor.execute(
        "DELETE FROM equipos WHERE activo = ?",
        (activo,),
    )


def insertar_equipo(cursor, datos):
    equipo = datos["equipo"]
    activo = equipo[0]

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
        equipo,
    )

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
        (activo, *datos["tecnica"]),
    )

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
        (activo, *datos["parametros"]),
    )

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
        (activo, *datos["configuracion"]),
    )

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
        (activo, *datos["regulatoria"]),
    )

    for mantenimiento in datos["mantenimientos"]:
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
            (activo, *mantenimiento),
        )

    for calibracion in datos["calibraciones"]:
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
            (activo, *calibracion),
        )

    for falla in datos["fallas"]:
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
            (activo, *falla),
        )

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
        (activo, *datos["indicadores"]),
    )

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
        (activo, *datos["economica"]),
    )

    ruta_manual = f"/static/manuales/{activo.lower()}.pdf"

    cursor.execute(
        """
        INSERT INTO documentos (
            activo,
            manual_usuario
        )
        VALUES (?, ?)
        """,
        (activo, ruta_manual),
    )

    ruta_equipo = f"/equipo/{activo}"

    cursor.execute(
        """
        INSERT INTO codigo_qr (
            activo,
            codigo_qr
        )
        VALUES (?, ?)
        """,
        (activo, ruta_equipo),
    )


def verificar_resultados(cursor):
    print("\n" + "=" * 70)
    print("VERIFICACIÓN DE EQUIPOS")
    print("=" * 70)

    for activo in ACTIVOS_NUEVOS:
        cursor.execute(
            """
            SELECT activo, nombre, marca, modelo, estado
            FROM equipos
            WHERE activo = ?
            """,
            (activo,),
        )

        equipo = cursor.fetchone()

        cursor.execute(
            "SELECT COUNT(*) FROM mantenimientos WHERE activo = ?",
            (activo,),
        )
        cantidad_mantenimientos = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM calibraciones WHERE activo = ?",
            (activo,),
        )
        cantidad_calibraciones = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM fallas WHERE activo = ?",
            (activo,),
        )
        cantidad_fallas = cursor.fetchone()[0]

        if equipo:
            print(
                f"{equipo[0]} | {equipo[1]} | {equipo[2]} {equipo[3]} | "
                f"Estado: {equipo[4]} | "
                f"Mantenimientos: {cantidad_mantenimientos} | "
                f"Calibraciones: {cantidad_calibraciones} | "
                f"Fallas: {cantidad_fallas}"
            )
        else:
            print(f"ERROR: No se encontró {activo}")


def cargar_equipos():
    if not RUTA_BASE_DATOS.exists():
        print(f"ERROR: No se encontró la base de datos: {RUTA_BASE_DATOS}")
        return

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.execute("PRAGMA foreign_keys = ON")
    cursor = conexion.cursor()

    try:
        print("=" * 70)
        print("CARGA DE EQUIPOS BIOTRACK V3")
        print("=" * 70)

        for datos in EQUIPOS:
            activo = datos["equipo"][0]

            print(f"Procesando {activo}...")

            eliminar_datos_existentes(cursor, activo)
            insertar_equipo(cursor, datos)

            print(f"{activo} cargado correctamente.")

        conexion.commit()

        verificar_resultados(cursor)

        print("\n" + "=" * 70)
        print("CARGA FINALIZADA CORRECTAMENTE")
        print("ACT-001 NO FUE MODIFICADO")
        print("=" * 70)

    except sqlite3.Error as error:
        conexion.rollback()

        print("\n" + "=" * 70)
        print("ERROR DURANTE LA CARGA")
        print("=" * 70)
        print(error)
        print("No se guardó ningún cambio.")

    finally:
        conexion.close()


if __name__ == "__main__":
    cargar_equipos()
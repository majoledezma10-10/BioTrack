import sqlite3
from datetime import date, datetime
from pathlib import Path

from correo import enviar_correo


CARPETA_PROYECTO = Path(__file__).resolve().parent
BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"

DIAS_AVISO = (30, 15, 7, 1, 0)


def convertir_fecha(valor):
    if not valor:
        return None

    try:
        return datetime.strptime(valor.strip(), "%Y-%m-%d").date()
    except (AttributeError, ValueError):
        return None


def crear_tabla_notificaciones(conexion):
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS notificaciones_enviadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            activo TEXT NOT NULL,
            fecha_evento TEXT NOT NULL,
            aviso TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            UNIQUE(tipo, activo, fecha_evento, aviso)
        )
    """)


def aviso_ya_enviado(
    conexion,
    tipo,
    activo,
    fecha_evento,
    aviso,
):
    resultado = conexion.execute(
        """
        SELECT 1
        FROM notificaciones_enviadas
        WHERE tipo = ?
          AND activo = ?
          AND fecha_evento = ?
          AND aviso = ?
        """,
        (
            tipo,
            activo,
            fecha_evento.isoformat(),
            aviso,
        ),
    ).fetchone()

    return resultado is not None


def registrar_aviso(
    conexion,
    tipo,
    activo,
    fecha_evento,
    aviso,
):
    conexion.execute(
        """
        INSERT OR IGNORE INTO notificaciones_enviadas (
            tipo,
            activo,
            fecha_evento,
            aviso,
            fecha_envio
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            tipo,
            activo,
            fecha_evento.isoformat(),
            aviso,
            date.today().isoformat(),
        ),
    )


def crear_texto_alerta(
    categoria,
    activo,
    nombre,
    fecha_evento,
    dias,
):
    equipo = f"{activo} - {nombre}"

    if dias > 1:
        return (
            f"{categoria} PRÓXIMA\n"
            f"Equipo: {equipo}\n"
            f"Fecha: {fecha_evento:%d/%m/%Y}\n"
            f"Faltan {dias} días."
        )

    if dias == 1:
        return (
            f"{categoria} PRÓXIMA\n"
            f"Equipo: {equipo}\n"
            f"Fecha: {fecha_evento:%d/%m/%Y}\n"
            "Falta 1 día."
        )

    if dias == 0:
        return (
            f"{categoria} PARA HOY\n"
            f"Equipo: {equipo}\n"
            f"Fecha: {fecha_evento:%d/%m/%Y}."
        )

    return (
        f"{categoria} VENCIDA\n"
        f"Equipo: {equipo}\n"
        f"Fecha: {fecha_evento:%d/%m/%Y}\n"
        f"Venció hace {-dias} días."
    )


def revisar_registros(
    conexion,
    consulta,
    columna_fecha,
    tipo,
    categoria,
):
    alertas = []
    avisos_pendientes = []
    hoy = date.today()

    registros = conexion.execute(consulta).fetchall()

    for registro in registros:
        fecha_evento = convertir_fecha(registro[columna_fecha])

        if fecha_evento is None:
            print(
                f"Fecha inválida omitida: "
                f"{registro['activo']} - "
                f"{registro[columna_fecha]}"
            )
            continue

        dias = (fecha_evento - hoy).days

        if dias in DIAS_AVISO:
            aviso = str(dias)

        elif dias < 0:
            aviso = "vencido"

        else:
            continue

        if aviso_ya_enviado(
            conexion,
            tipo,
            registro["activo"],
            fecha_evento,
            aviso,
        ):
            continue

        alertas.append(
            crear_texto_alerta(
                categoria,
                registro["activo"],
                registro["nombre"],
                fecha_evento,
                dias,
            )
        )

        avisos_pendientes.append(
            (
                tipo,
                registro["activo"],
                fecha_evento,
                aviso,
            )
        )

    return alertas, avisos_pendientes


def ejecutar_recordatorios():
    with sqlite3.connect(BASE_DATOS) as conexion:
        conexion.row_factory = sqlite3.Row
        crear_tabla_notificaciones(conexion)

        consulta_mantenimientos = """
            SELECT
                e.activo,
                e.nombre,
                m.proximo_mantenimiento
            FROM mantenimientos AS m
            INNER JOIN equipos AS e
                ON e.activo = m.activo
            WHERE m.id = (
                SELECT MAX(m2.id)
                FROM mantenimientos AS m2
                WHERE m2.activo = m.activo
            )
            AND m.proximo_mantenimiento IS NOT NULL
            AND TRIM(m.proximo_mantenimiento) != ''
            ORDER BY e.activo
        """

        consulta_calibraciones = """
            SELECT
                e.activo,
                e.nombre,
                c.proxima_calibracion
            FROM calibraciones AS c
            INNER JOIN equipos AS e
                ON e.activo = c.activo
            WHERE c.id = (
                SELECT MAX(c2.id)
                FROM calibraciones AS c2
                WHERE c2.activo = c.activo
            )
            AND c.proxima_calibracion IS NOT NULL
            AND TRIM(c.proxima_calibracion) != ''
            ORDER BY e.activo
        """

        mantenimientos, avisos_mantenimiento = revisar_registros(
            conexion,
            consulta_mantenimientos,
            "proximo_mantenimiento",
            "mantenimiento",
            "MANTENIMIENTO",
        )

        calibraciones, avisos_calibracion = revisar_registros(
            conexion,
            consulta_calibraciones,
            "proxima_calibracion",
            "calibracion",
            "CALIBRACIÓN",
        )

        alertas = mantenimientos + calibraciones
        avisos_pendientes = (
            avisos_mantenimiento + avisos_calibracion
        )

        if not alertas:
            print("No hay alertas nuevas para enviar.")
            return

        contenido = (
            "RESUMEN DE ALERTAS DE BIOTRACK\n"
            "================================\n\n"
            + "\n\n--------------------------------\n\n".join(alertas)
            + "\n\nIngresá a BioTrack para revisar los equipos."
        )

        enviar_correo(
            asunto=f"BioTrack - Resumen de {len(alertas)} alertas",
            contenido=contenido,
        )

        for tipo, activo, fecha_evento, aviso in avisos_pendientes:
            registrar_aviso(
                conexion,
                tipo,
                activo,
                fecha_evento,
                aviso,
            )

        conexion.commit()

    print(f"Correo resumen enviado con {len(alertas)} alertas.")


if __name__ == "__main__":
    ejecutar_recordatorios()
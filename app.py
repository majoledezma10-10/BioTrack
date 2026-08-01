from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path
import os
from dotenv import load_dotenv
import sqlite3

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "BIOTRACK_SECRET_KEY",
    "biotrack-clave-local-cambiar-al-publicar",
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.permanent_session_lifetime = timedelta(hours=8)

CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "database" / "biotrack_v2.db"

DIAS_ALERTA = 30


def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def convertir_fecha(valor):
    """
    Convierte una fecha YYYY-MM-DD en un objeto date.

    Devuelve None cuando el campo está vacío o contiene textos como
    'Pendiente de reparación'.
    """
    if not valor:
        return None

    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def formatear_fecha(fecha):
    if fecha is None:
        return "Fecha no disponible"

    return fecha.strftime("%d/%m/%Y")
def obtener_usuario_actual():
    if "usuario_id" not in session:
        return None

    return {
        "id": session.get("usuario_id"),
        "nombre": session.get("nombre"),
        "nombre_usuario": session.get("nombre_usuario"),
        "rol": session.get("rol"),
    }


def login_requerido(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            session["pagina_pendiente"] = request.path
            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return envoltura


def roles_requeridos(*roles_permitidos):
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            if "usuario_id" not in session:
                session["pagina_pendiente"] = request.path
                return redirect(url_for("login"))

            if session.get("rol") not in roles_permitidos:
                return (
                    render_template(
                        "acceso_denegado.html",
                        usuario_actual=obtener_usuario_actual(),
                    ),
                    403,
                )

            return funcion(*args, **kwargs)

        return envoltura

    return decorador

def obtener_panel_alarmas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    hoy = date.today()
    limite_alerta = hoy + timedelta(days=DIAS_ALERTA)

    alertas_criticas = []
    equipos_mantenimiento = []
    mantenimientos_vencidos = []
    mantenimientos_proximos = []
    calibraciones_vencidas = []
    calibraciones_proximas = []
    garantias_vencidas = []
    garantias_proximas = []

    try:
        # RESUMEN DE EQUIPOS
        cursor.execute(
            """
            SELECT activo, nombre, marca, modelo, estado, criticidad
            FROM equipos
            ORDER BY activo
            """
        )
        equipos = cursor.fetchall()

        resumen = {
            "total": len(equipos),
            "operativos": 0,
            "mantenimiento": 0,
            "fuera_servicio": 0,
        }

        for equipo in equipos:
            estado_original = equipo["estado"] or ""
            estado = estado_original.strip().lower()

            datos_equipo = {
                "activo": equipo["activo"],
                "nombre": equipo["nombre"],
                "marca": equipo["marca"],
                "modelo": equipo["modelo"],
                "estado": estado_original,
                "criticidad": equipo["criticidad"],
            }

            if "fuera de servicio" in estado:
                resumen["fuera_servicio"] += 1
                alertas_criticas.append(datos_equipo)

            elif "mantenimiento" in estado or "en pausa" in estado:
                resumen["mantenimiento"] += 1
                equipos_mantenimiento.append(datos_equipo)

            else:
                resumen["operativos"] += 1

        # MANTENIMIENTOS
        for equipo in equipos:
            activo = equipo["activo"]

            cursor.execute(
                """
                SELECT proximo_mantenimiento
                FROM mantenimientos
                WHERE activo = ?
                ORDER BY fecha DESC, id DESC
                LIMIT 1
                """,
                (activo,),
            )
            mantenimiento = cursor.fetchone()

            if mantenimiento is None:
                continue

            fecha_mantenimiento = convertir_fecha(
                mantenimiento["proximo_mantenimiento"]
            )

            if fecha_mantenimiento is None:
                continue

            alerta = {
                "activo": activo,
                "nombre": equipo["nombre"],
                "fecha": fecha_mantenimiento,
                "fecha_texto": formatear_fecha(fecha_mantenimiento),
                "dias": (fecha_mantenimiento - hoy).days,
            }

            if fecha_mantenimiento < hoy:
                mantenimientos_vencidos.append(alerta)

            elif fecha_mantenimiento <= limite_alerta:
                mantenimientos_proximos.append(alerta)

        # CALIBRACIONES
        for equipo in equipos:
            activo = equipo["activo"]

            cursor.execute(
                """
                SELECT proxima_calibracion
                FROM calibraciones
                WHERE activo = ?
                ORDER BY fecha DESC, id DESC
                LIMIT 1
                """,
                (activo,),
            )
            calibracion = cursor.fetchone()

            if calibracion is None:
                continue

            fecha_calibracion = convertir_fecha(
                calibracion["proxima_calibracion"]
            )

            if fecha_calibracion is None:
                continue

            alerta = {
                "activo": activo,
                "nombre": equipo["nombre"],
                "fecha": fecha_calibracion,
                "fecha_texto": formatear_fecha(fecha_calibracion),
                "dias": (fecha_calibracion - hoy).days,
            }

            if fecha_calibracion < hoy:
                calibraciones_vencidas.append(alerta)

            elif fecha_calibracion <= limite_alerta:
                calibraciones_proximas.append(alerta)

        # GARANTÍAS
        cursor.execute(
            """
            SELECT
                e.activo,
                e.nombre,
                ie.vencimiento_garantia
            FROM equipos AS e
            INNER JOIN informacion_economica AS ie
                ON ie.activo = e.activo
            ORDER BY e.activo
            """
        )
        registros_garantia = cursor.fetchall()

        for registro in registros_garantia:
            fecha_garantia = convertir_fecha(
                registro["vencimiento_garantia"]
            )

            if fecha_garantia is None:
                continue

            alerta = {
                "activo": registro["activo"],
                "nombre": registro["nombre"],
                "fecha": fecha_garantia,
                "fecha_texto": formatear_fecha(fecha_garantia),
                "dias": (fecha_garantia - hoy).days,
            }

            if fecha_garantia < hoy:
                garantias_vencidas.append(alerta)

            elif fecha_garantia <= limite_alerta:
                garantias_proximas.append(alerta)

        # Ordenar las alertas por fecha.
        mantenimientos_vencidos.sort(key=lambda item: item["fecha"])
        mantenimientos_proximos.sort(key=lambda item: item["fecha"])
        calibraciones_vencidas.sort(key=lambda item: item["fecha"])
        calibraciones_proximas.sort(key=lambda item: item["fecha"])
        garantias_vencidas.sort(key=lambda item: item["fecha"])
        garantias_proximas.sort(key=lambda item: item["fecha"])

        cantidad_alertas = (
            len(alertas_criticas)
            + len(equipos_mantenimiento)
            + len(mantenimientos_vencidos)
            + len(mantenimientos_proximos)
            + len(calibraciones_vencidas)
            + len(calibraciones_proximas)
            + len(garantias_vencidas)
            + len(garantias_proximas)
        )

        return {
            "resumen": resumen,
            "alertas_criticas": alertas_criticas,
            "equipos_mantenimiento": equipos_mantenimiento,
            "mantenimientos_vencidos": mantenimientos_vencidos,
            "mantenimientos_proximos": mantenimientos_proximos,
            "calibraciones_vencidas": calibraciones_vencidas,
            "calibraciones_proximas": calibraciones_proximas,
            "garantias_vencidas": garantias_vencidas,
            "garantias_proximas": garantias_proximas,
            "cantidad_alertas": cantidad_alertas,
            "fecha_actual": formatear_fecha(hoy),
        }

    finally:
        conexion.close()


def obtener_datos_equipo(activo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "SELECT * FROM equipos WHERE activo = ?",
            (activo,),
        )
        equipo = cursor.fetchone()

        if equipo is None:
            return None

        cursor.execute(
            "SELECT * FROM informacion_tecnica WHERE activo = ?",
            (activo,),
        )
        informacion_tecnica = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM parametros_monitorizados WHERE activo = ?",
            (activo,),
        )
        parametros = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM configuracion WHERE activo = ?",
            (activo,),
        )
        configuracion = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM informacion_regulatoria WHERE activo = ?",
            (activo,),
        )
        informacion_regulatoria = cursor.fetchone()

        cursor.execute(
            """
            SELECT *
            FROM mantenimientos
            WHERE activo = ?
            ORDER BY fecha DESC, id DESC
            """,
            (activo,),
        )
        mantenimientos = cursor.fetchall()

        cursor.execute(
            """
            SELECT *
            FROM calibraciones
            WHERE activo = ?
            ORDER BY fecha DESC, id DESC
            """,
            (activo,),
        )
        calibraciones = cursor.fetchall()

        cursor.execute(
            """
            SELECT *
            FROM fallas
            WHERE activo = ?
            ORDER BY fecha DESC, id DESC
            """,
            (activo,),
        )
        fallas = cursor.fetchall()

        cursor.execute(
            "SELECT * FROM indicadores WHERE activo = ?",
            (activo,),
        )
        indicadores = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM informacion_economica WHERE activo = ?",
            (activo,),
        )
        informacion_economica = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM documentos WHERE activo = ?",
            (activo,),
        )
        documentos = cursor.fetchone()

        print("\n" + "=" * 60)
        print(f"DATOS CONSULTADOS PARA {activo}")
        print(f"Base de datos: {RUTA_BASE_DATOS}")
        print(f"Mantenimientos: {len(mantenimientos)}")
        print(f"Calibraciones: {len(calibraciones)}")
        print(f"Fallas: {len(fallas)}")
        print(f"Indicadores: {'Sí' if indicadores else 'No'}")
        print(
            "Información económica: "
            f"{'Sí' if informacion_economica else 'No'}"
        )
        print("=" * 60)

        return {
            "equipo": equipo,
            "informacion_tecnica": informacion_tecnica,
            "parametros": parametros,
            "configuracion": configuracion,
            "informacion_regulatoria": informacion_regulatoria,
            "mantenimientos": mantenimientos,
            "calibraciones": calibraciones,
            "fallas": fallas,
            "indicadores": indicadores,
            "informacion_economica": informacion_economica,
            "documentos": documentos,
            "imagen_equipo": f"images/{activo.lower()}.jpg",
            "imagen_qr": f"qr/{activo.lower()}.png",
        }

    finally:
        conexion.close()


def renderizar_pagina(
    equipo=None,
    mensaje=None,
    codigo_estado=200,
    **datos_equipo,
):
    panel = obtener_panel_alarmas()
    usuario_actual = obtener_usuario_actual()
    rol = session.get("rol")

    return (
        render_template(
            "index.html",
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=usuario_actual,
            puede_registrar=rol in ("administrador", "usuario"),
            es_administrador=rol == "administrador",
            es_visitante=rol == "visitante",
            **panel,
            **datos_equipo,
        ),
        codigo_estado,
    )


def procesar_busqueda():
    activo = request.form.get("activo", "").strip().upper()

    if not activo:
        return renderizar_pagina(
            equipo=None,
            mensaje="Ingrese un número de activo.",
        )

    return redirect(url_for("ver_equipo", activo=activo))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("inicio"))

    mensaje = None

    if request.method == "POST":
        nombre_usuario = (
            request.form.get("nombre_usuario", "")
            .strip()
            .lower()
        )
        contrasena = request.form.get("contrasena", "")

        if not nombre_usuario or not contrasena:
            mensaje = "Ingrese el usuario y la contraseña."

        else:
            conexion = obtener_conexion()

            try:
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        nombre_usuario,
                        contrasena_hash,
                        rol,
                        activo
                    FROM usuarios
                    WHERE nombre_usuario = ?
                    """,
                    (nombre_usuario,),
                )

                usuario = cursor.fetchone()

                credenciales_validas = (
                    usuario is not None
                    and usuario["activo"] == 1
                    and check_password_hash(
                        usuario["contrasena_hash"],
                        contrasena,
                    )
                )

                if not credenciales_validas:
                    mensaje = "Usuario o contraseña incorrectos."

                else:
                    fecha_acceso = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    cursor.execute(
                        """
                        UPDATE usuarios
                        SET ultimo_acceso = ?
                        WHERE id = ?
                        """,
                        (
                            fecha_acceso,
                            usuario["id"],
                        ),
                    )

                    conexion.commit()

                    pagina_pendiente = session.get("pagina_pendiente")

                    session.clear()
                    session.permanent = True

                    session["usuario_id"] = usuario["id"]
                    session["nombre"] = usuario["nombre"]
                    session["nombre_usuario"] = usuario["nombre_usuario"]
                    session["rol"] = usuario["rol"]

                    if pagina_pendiente:
                        return redirect(pagina_pendiente)

                    return redirect(url_for("inicio"))


            except sqlite3.Error as error:
                conexion.rollback()
                print(f"Error durante el inicio de sesión: {error}")
                mensaje = "No fue posible iniciar sesión."

            finally:
                conexion.close()

    return render_template(
        "login.html",
        mensaje=mensaje,
    )


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_requerido
def inicio():
    if request.method == "POST":
        return procesar_busqueda()

    return renderizar_pagina(
        equipo=None,
        mensaje=None,
    )


@app.route("/equipo/<activo>", methods=["GET", "POST"])
@login_requerido
def ver_equipo(activo):
    if request.method == "POST":
        return procesar_busqueda()

    activo = activo.strip().upper()
    datos = obtener_datos_equipo(activo)

    if datos is None:
        return renderizar_pagina(
            equipo=None,
            mensaje=f"No se encontró el equipo {activo}.",
            codigo_estado=404,
        )

    equipo = datos.pop("equipo")

    return renderizar_pagina(
        equipo=equipo,
        mensaje=None,
        **datos,
    )

@app.route(
    "/equipo/<activo>/registrar-mantenimiento",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador", "usuario")
def registrar_mantenimiento(activo):
    activo = activo.strip().upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (activo,),
        )
        equipo = cursor.fetchone()

        if equipo is None:
            return redirect(url_for("inicio"))

        mensaje = None

        if request.method == "POST":
            fecha = request.form.get("fecha", "").strip()
            tipo = request.form.get("tipo", "").strip()
            tecnico = request.form.get(
                "tecnico_responsable",
                "",
            ).strip()
            descripcion = request.form.get(
                "descripcion",
                "",
            ).strip()
            repuestos = request.form.get(
                "repuestos_utilizados",
                "",
            ).strip()
            proximo = request.form.get(
                "proximo_mantenimiento",
                "",
            ).strip()

            if not fecha or not tipo or not tecnico or not descripcion:
                mensaje = "Complete todos los campos obligatorios."

            else:
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
                    (
                        activo,
                        fecha,
                        tipo,
                        tecnico,
                        descripcion,
                        repuestos or "No aplica",
                        proximo or None,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for("ver_equipo", activo=activo)
                )

        return render_template(
            "registrar_mantenimiento.html",
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al registrar mantenimiento: {error}")

        return render_template(
            "registrar_mantenimiento.html",
            equipo=equipo,
            mensaje="No fue posible guardar el mantenimiento.",
            usuario_actual=obtener_usuario_actual(),
        )

    finally:
        conexion.close()
@app.route(
    "/mantenimiento/<int:mantenimiento_id>/editar",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador")
def editar_mantenimiento(mantenimiento_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM mantenimientos
            WHERE id = ?
            """,
            (mantenimiento_id,),
        )
        mantenimiento = cursor.fetchone()

        if mantenimiento is None:
            return redirect(url_for("inicio"))

        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (mantenimiento["activo"],),
        )
        equipo = cursor.fetchone()

        mensaje = None

        if request.method == "POST":
            fecha = request.form.get("fecha", "").strip()
            tipo = request.form.get("tipo", "").strip()
            tecnico = request.form.get(
                "tecnico_responsable",
                "",
            ).strip()
            descripcion = request.form.get(
                "descripcion",
                "",
            ).strip()
            repuestos = request.form.get(
                "repuestos_utilizados",
                "",
            ).strip()
            proximo = request.form.get(
                "proximo_mantenimiento",
                "",
            ).strip()

            if not fecha or not tipo or not tecnico or not descripcion:
                mensaje = "Complete todos los campos obligatorios."

            else:
                cursor.execute(
                    """
                    UPDATE mantenimientos
                    SET
                        fecha = ?,
                        tipo = ?,
                        tecnico_responsable = ?,
                        descripcion = ?,
                        repuestos_utilizados = ?,
                        proximo_mantenimiento = ?
                    WHERE id = ?
                    """,
                    (
                        fecha,
                        tipo,
                        tecnico,
                        descripcion,
                        repuestos or "No aplica",
                        proximo or None,
                        mantenimiento_id,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for(
                        "ver_equipo",
                        activo=mantenimiento["activo"],
                    )
                )

        return render_template(
            "editar_mantenimiento.html",
            mantenimiento=mantenimiento,
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al editar mantenimiento: {error}")

        return redirect(url_for("inicio"))

    finally:
        conexion.close()


@app.route(
    "/mantenimiento/<int:mantenimiento_id>/eliminar",
    methods=["POST"],
)
@roles_requeridos("administrador")
def eliminar_mantenimiento(mantenimiento_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo
            FROM mantenimientos
            WHERE id = ?
            """,
            (mantenimiento_id,),
        )
        mantenimiento = cursor.fetchone()

        if mantenimiento is None:
            return redirect(url_for("inicio"))

        activo = mantenimiento["activo"]

        cursor.execute(
            """
            DELETE FROM mantenimientos
            WHERE id = ?
            """,
            (mantenimiento_id,),
        )

        conexion.commit()

        return redirect(
            url_for("ver_equipo", activo=activo)
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al eliminar mantenimiento: {error}")

        return redirect(url_for("inicio"))

    finally:
        conexion.close()

@app.route(
    "/equipo/<activo>/registrar-calibracion",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador", "usuario")
def registrar_calibracion(activo):
    activo = activo.strip().upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (activo,),
        )
        equipo = cursor.fetchone()

        if equipo is None:
            return redirect(url_for("inicio"))

        mensaje = None

        if request.method == "POST":
            fecha = request.form.get("fecha", "").strip()
            resultado = request.form.get("resultado", "").strip()
            certificado = request.form.get("certificado", "").strip()
            patron = request.form.get(
                "patron_utilizado",
                "",
            ).strip()
            proxima = request.form.get(
                "proxima_calibracion",
                "",
            ).strip()

            if not fecha or not resultado or not certificado or not patron:
                mensaje = "Complete todos los campos obligatorios."

            else:
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
                    (
                        activo,
                        fecha,
                        resultado,
                        certificado,
                        patron,
                        proxima or None,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for("ver_equipo", activo=activo)
                )

        return render_template(
            "registrar_calibracion.html",
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al registrar calibración: {error}")

        return render_template(
            "registrar_calibracion.html",
            equipo=equipo,
            mensaje="No fue posible guardar la calibración.",
            usuario_actual=obtener_usuario_actual(),
        )

    finally:
        conexion.close()

@app.route(
    "/calibracion/<int:calibracion_id>/editar",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador")
def editar_calibracion(calibracion_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM calibraciones
            WHERE id = ?
            """,
            (calibracion_id,),
        )
        calibracion = cursor.fetchone()

        if calibracion is None:
            return redirect(url_for("inicio"))

        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (calibracion["activo"],),
        )
        equipo = cursor.fetchone()

        mensaje = None

        if request.method == "POST":
            fecha = request.form.get("fecha", "").strip()
            resultado = request.form.get("resultado", "").strip()
            certificado = request.form.get("certificado", "").strip()
            patron = request.form.get(
                "patron_utilizado",
                "",
            ).strip()
            proxima = request.form.get(
                "proxima_calibracion",
                "",
            ).strip()

            if not fecha or not resultado or not certificado or not patron:
                mensaje = "Complete todos los campos obligatorios."

            else:
                cursor.execute(
                    """
                    UPDATE calibraciones
                    SET
                        fecha = ?,
                        resultado = ?,
                        certificado = ?,
                        patron_utilizado = ?,
                        proxima_calibracion = ?
                    WHERE id = ?
                    """,
                    (
                        fecha,
                        resultado,
                        certificado,
                        patron,
                        proxima or None,
                        calibracion_id,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for(
                        "ver_equipo",
                        activo=calibracion["activo"],
                    )
                )

        return render_template(
            "editar_calibracion.html",
            calibracion=calibracion,
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al editar calibración: {error}")
        return redirect(url_for("inicio"))

    finally:
        conexion.close()


@app.route(
    "/calibracion/<int:calibracion_id>/eliminar",
    methods=["POST"],
)
@roles_requeridos("administrador")
def eliminar_calibracion(calibracion_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo
            FROM calibraciones
            WHERE id = ?
            """,
            (calibracion_id,),
        )
        calibracion = cursor.fetchone()

        if calibracion is None:
            return redirect(url_for("inicio"))

        activo = calibracion["activo"]

        cursor.execute(
            """
            DELETE FROM calibraciones
            WHERE id = ?
            """,
            (calibracion_id,),
        )

        conexion.commit()

        return redirect(
            url_for("ver_equipo", activo=activo)
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al eliminar calibración: {error}")
        return redirect(url_for("inicio"))

    finally:
        conexion.close()

@app.route(
    "/equipo/<activo>/registrar-falla",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador", "usuario")
def registrar_falla(activo):
    activo = activo.strip().upper()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (activo,),
        )

        equipo = cursor.fetchone()

        if equipo is None:
            return redirect(url_for("inicio"))

        mensaje = None

        if request.method == "POST":

            fecha = request.form.get("fecha", "").strip()
            falla = request.form.get("falla_reportada", "").strip()
            diagnostico = request.form.get("diagnostico", "").strip()
            accion = request.form.get("accion_realizada", "").strip()
            tiempo = request.form.get(
                "tiempo_fuera_servicio",
                "",
            ).strip()

            if not fecha or not falla or not diagnostico or not accion:
                mensaje = "Complete todos los campos obligatorios."

            else:

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
                    (
                        activo,
                        fecha,
                        falla,
                        diagnostico,
                        accion,
                        tiempo,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for(
                        "ver_equipo",
                        activo=activo,
                    )
                )

        return render_template(
            "registrar_falla.html",
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:

        conexion.rollback()

        print(error)

        return render_template(
            "registrar_falla.html",
            equipo=equipo,
            mensaje="No fue posible registrar la falla.",
            usuario_actual=obtener_usuario_actual(),
        )

    finally:
        conexion.close()

@app.route(
    "/falla/<int:falla_id>/editar",
    methods=["GET", "POST"],
)
@roles_requeridos("administrador")
def editar_falla(falla_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM fallas
            WHERE id = ?
            """,
            (falla_id,),
        )
        falla = cursor.fetchone()

        if falla is None:
            return redirect(url_for("inicio"))

        cursor.execute(
            """
            SELECT activo, nombre
            FROM equipos
            WHERE activo = ?
            """,
            (falla["activo"],),
        )
        equipo = cursor.fetchone()

        mensaje = None

        if request.method == "POST":
            fecha = request.form.get("fecha", "").strip()
            falla_reportada = request.form.get(
                "falla_reportada",
                "",
            ).strip()
            diagnostico = request.form.get(
                "diagnostico",
                "",
            ).strip()
            accion = request.form.get(
                "accion_realizada",
                "",
            ).strip()
            tiempo = request.form.get(
                "tiempo_fuera_servicio",
                "",
            ).strip()

            if (
                not fecha
                or not falla_reportada
                or not diagnostico
                or not accion
                or not tiempo
            ):
                mensaje = "Complete todos los campos obligatorios."

            else:
                cursor.execute(
                    """
                    UPDATE fallas
                    SET
                        fecha = ?,
                        falla_reportada = ?,
                        diagnostico = ?,
                        accion_realizada = ?,
                        tiempo_fuera_servicio = ?
                    WHERE id = ?
                    """,
                    (
                        fecha,
                        falla_reportada,
                        diagnostico,
                        accion,
                        tiempo,
                        falla_id,
                    ),
                )

                conexion.commit()

                return redirect(
                    url_for(
                        "ver_equipo",
                        activo=falla["activo"],
                    )
                )

        return render_template(
            "editar_falla.html",
            falla=falla,
            equipo=equipo,
            mensaje=mensaje,
            usuario_actual=obtener_usuario_actual(),
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al editar falla: {error}")
        return redirect(url_for("inicio"))

    finally:
        conexion.close()


@app.route(
    "/falla/<int:falla_id>/eliminar",
    methods=["POST"],
)
@roles_requeridos("administrador")
def eliminar_falla(falla_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            SELECT activo
            FROM fallas
            WHERE id = ?
            """,
            (falla_id,),
        )
        falla = cursor.fetchone()

        if falla is None:
            return redirect(url_for("inicio"))

        activo = falla["activo"]

        cursor.execute(
            """
            DELETE FROM fallas
            WHERE id = ?
            """,
            (falla_id,),
        )

        conexion.commit()

        return redirect(
            url_for("ver_equipo", activo=activo)
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al eliminar falla: {error}")
        return redirect(url_for("inicio"))

    finally:
        conexion.close()


if __name__ == "__main__":
    print(f"Base de datos utilizada: {RUTA_BASE_DATOS}")
    app.run(debug=True)
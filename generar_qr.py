from pathlib import Path

try:
    import qrcode
except ImportError:
    print("ERROR: Falta instalar la librería qrcode.")
    print("Ejecutá: py -m pip install qrcode[pil]")
    raise SystemExit(1)


CARPETA_PROYECTO = Path(__file__).resolve().parent
CARPETA_QR = CARPETA_PROYECTO / "static" / "qr"

# Mientras BioTrack funciona localmente:
URL_BASE = "http://127.0.0.1:5000"

ACTIVOS = (
    "ACT-001",
    "ACT-002",
    "ACT-003",
    "ACT-004",
    "ACT-005",
    "ACT-006",
)


def generar_codigos_qr() -> None:
    CARPETA_QR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("GENERANDO CÓDIGOS QR DE BIOTRACK")
    print("=" * 60)

    for activo in ACTIVOS:
        url_equipo = f"{URL_BASE}/equipo/{activo}"
        nombre_archivo = f"{activo.lower()}.png"
        ruta_salida = CARPETA_QR / nombre_archivo

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(url_equipo)
        qr.make(fit=True)

        imagen = qr.make_image(
            fill_color="#0f4c5c",
            back_color="white",
        )

        imagen.save(ruta_salida)

        print(f"{activo}: {ruta_salida.name}")
        print(f"Enlace: {url_equipo}")

    print("=" * 60)
    print(f"QR guardados en: {CARPETA_QR}")
    print("=" * 60)


if __name__ == "__main__":
    generar_codigos_qr()
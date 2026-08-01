import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


def enviar_correo(asunto: str, contenido: str) -> None:
    remitente = os.getenv("EMAIL_REMITENTE", "").strip()
    password = os.getenv("EMAIL_PASSWORD", "").replace(" ", "")
    destinatarios = [
        correo.strip()
        for correo in os.getenv("EMAIL_DESTINOS", "").split(",")
        if correo.strip()
    ]

    if not remitente or not password or not destinatarios:
        raise ValueError("Faltan datos de correo en el archivo .env")

    mensaje = EmailMessage()
    mensaje["Subject"] = asunto
    mensaje["From"] = f"BioTrack <{remitente}>"
    mensaje["To"] = ", ".join(destinatarios)
    mensaje.set_content(contenido)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, password)
        servidor.send_message(mensaje)


if __name__ == "__main__":
    enviar_correo(
        asunto="Prueba de notificaciones BioTrack",
        contenido=(
            "¡Hola!\n\n"
            "Este es un correo de prueba enviado correctamente desde BioTrack.\n\n"
            "Las notificaciones ya están funcionando."
        ),
    )

    print("Correo enviado correctamente.")
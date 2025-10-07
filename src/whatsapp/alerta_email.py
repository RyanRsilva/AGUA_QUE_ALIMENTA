import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USERNAME)
EMAIL_TO = os.getenv("EMAIL_TO", "admin@yourdomain.com")

logger = logging.getLogger(__name__)


def enviar_alerta_email(subject, message):
    """
    Envia um alerta por email como fallback.
    """
    if not EMAIL_USERNAME or EMAIL_USERNAME == "your-email@gmail.com":
        logger.error("Configuração de email não definida")
        return False

    try:
        # Criar mensagem
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Conectar ao servidor SMTP
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()

        logger.info(f"Alerta enviado por email para {EMAIL_TO}")
        return True
    except Exception as e:
        logger.error(f"Falha ao enviar email: {e}")
        return False


# --- Bloco de Teste ---
if __name__ == '__main__':
    print("--- Testando o módulo de alerta por email ---")
    subject = "Teste de Alerta - Sistema Água que Alimenta"
    message = "Este é um teste do sistema de alertas por email."
    enviar_alerta_email(subject, message)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import config_by_name
import os
import traceback
import logging

logger = logging.getLogger(__name__)


def send_password_reset_email(to_email, reset_token):
    env = os.getenv("ENV", "development")
    configuration = config_by_name.get(env)
    try:
        # Configurar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Redefinição de Senha"
        message["From"] = configuration.MAIL_USERNAME
        message["To"] = to_email

        # URL para redefinição de senha
        reset_url = f"{configuration.FRONT_URL}/reset-password/{reset_token}"

        # Criar versão texto e HTML do email
        text = f"""
        Olá,
        
        Você solicitou a redefinição de sua senha. Por favor, clique no link abaixo para redefini-la:
        
        {reset_url}
        
        Este link é válido por 1 hora.
        
        Se você não solicitou esta redefinição, por favor ignore este email.
        """

        html = f"""
        <html>
          <body>
            <h2>Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Você solicitou a redefinição de sua senha. Por favor, clique no link abaixo para redefini-la:</p>
            <p><a href="{reset_url}">Redefinir minha senha</a></p>
            <p>Ou copie e cole o seguinte link em seu navegador:</p>
            <p>{reset_url}</p>
            <p>Este link é válido por 1 hora.</p>
            <p>Se você não solicitou esta redefinição, por favor ignore este email.</p>
          </body>
        </html>
        """

        # Anexar partes à mensagem
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Conectar ao servidor SMTP e enviar email
        with smtplib.SMTP(configuration.MAIL_SERVER, configuration.MAIL_PORT) as server:
            server.starttls()
            server.login(configuration.MAIL_USERNAME, configuration.MAIL_PASSWORD)
            server.sendmail(configuration.MAIL_USERNAME, to_email, message.as_string())

        return True
    except Exception as e:
        logger.error(traceback.format_exc())
        print(f"Erro ao enviar email: {str(e)}")
        return False

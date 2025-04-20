import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import BaseConfig as Config


def send_password_reset_email(to_email, reset_token):
    try:
        # Configurar mensagem
        message = MIMEMultipart("alternative")
        message["Subject"] = "Redefinição de Senha"
        message["From"] = Config.SMTP_USERNAME
        message["To"] = to_email

        # URL para redefinição de senha
        reset_url = f"{Config.APP_BASE_URL}/reset-password/{reset_token}"

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
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USERNAME, to_email, message.as_string())

        return True
    except Exception as e:
        print(f"Erro ao enviar email: {str(e)}")
        return False

import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from app.core.config import settings, Logger

class MailService:
    def __init__(self, smtp_server: str = settings.SMTP_HOST, smtp_port: int = settings.SMTP_PORT, smtp_user: str = settings.SMTP_USER, smtp_password: str = settings.SMTP_PASSWORD):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.logger = Logger(__name__).get_logger() # Logger instance

    async def send_email(self, recipient: str, subject: str, body: str = None, template_name: str = None, context: dict = None):
        """
        Send an email with either a custom body or using a Jinja2 template.
        Args:
            recipient (str): Email recipient.
            subject (str): Subject of the email.
            body (str): Plain text body (optional if template is provided).
            template_name (str): Template name if email should use a template (optional).
            context (dict): Context for template rendering (optional).
            db (Session): Database session for transaction management (optional).
        """
        try:
            # If template_name is provided, render the template with context
            if template_name:
                # Render the template
                template_env = Environment(loader=FileSystemLoader('templates'))
                template = template_env.get_template(template_name)

                # Use context if available, otherwise an empty dict
                email_body = template.render(context or {})
            else:
                # If no template, use the plain text body
                email_body = body

            # Setup the email message
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = recipient
            msg.set_content("This email requires HTML support.")  # Fallback content for non-HTML email clients
            msg.add_alternative(email_body, subtype='html')

            # Sending email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"Email sent to {recipient} successfully.")

        except Exception as e:
            print(f"Failed to send email: {e}")
            raise Exception(f"Failed to send email: {e}")

    async def send_otp_email(self, name: str, email: str, otp: str, expiration_time: datetime, ip_address: str,):
        """
        Specialized method to send OTP email using a template.
        """
        self.logger.info(f"Sending OTP email to {email} from IP address {ip_address}.")
        
        # Setup email context
        context = {
            'name': name,
            'otp': otp,  # Send plain OTP in the email body
            'expiration_time': expiration_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            'ip_address': ip_address,
            'server_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            'company_name': settings.APP_NAME,
        }

        try:
            # Send email using the general send_email method, with a template for OTP
            await self.send_email(
                recipient=email,
                subject="Your OTP Code",
                template_name='otp_email_template.html',  # Template for OTP
                context=context,
            )

            self.logger.info(f"OTP email sent to {email} successfully.")

        except Exception as e:
            self.logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            raise Exception(f"Failed to send OTP email: {str(e)}")

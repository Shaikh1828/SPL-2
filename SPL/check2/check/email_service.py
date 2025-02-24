import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL, EMAIL_PASSWORD

class EmailService:
    @staticmethod
    def send_verification_email(to_email, verification_code):
        try:
            smtp_server = "smtp.gmail.com"
            port = 587
            
            message = MIMEMultipart("alternative")
            message["Subject"] = "Email Verification - Droid Scanner"
            message["From"] = EMAIL
            message["To"] = to_email

            html_content = f"""
            <html>
              <body>
                <h2>Welcome to Droid Scanner!</h2>
                <p>Your verification code is: <strong>{verification_code}</strong></p>
                <p>Please enter this code in the application to complete your registration.</p>
              </body>
            </html>
            """

            message.attach(MIMEText(html_content, "html"))

            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(message)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
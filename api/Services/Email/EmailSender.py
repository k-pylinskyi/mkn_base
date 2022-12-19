import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class EmailSender:
    # 'k.pylinskyi@gmail.com',
    # 'polinap5411@gmail.com',
    def __init__(self):
        self.port = 465
        self.login = "prices.mnk.group@gmail.com"
        self.password = "hrsvhqkajsdjtyzr"
        self.addresses = [
            'mykyta.karant@gmail.com'
        ]

    def send(self, html_message):
        # Create a secure SSL context
        context = ssl.create_default_context()

        for mail_to in self.addresses:
            msg = MIMEMultipart('alternative')
            today = datetime.today().strftime("%d-%m-%Y")
            msg['Subject'] = f"DB Update report {today}"
            msg['From'] = self.login
            msg['To'] = mail_to

            part = MIMEText(html_message, 'html')
            msg.attach(part)

            with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
                server.login(self.login, self.password)
                server.sendmail(self.login, mail_to, msg.as_string())
                server.quit()
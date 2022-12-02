import smtplib, ssl

class EmailSender:
    def __init__(self):
        self.port = 465
        self.login = "prices.mnk.group@gmail.com"
        self.password = "hrsvhqkajsdjtyzr"

    def send(self, receiver_email, message):
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login(self.login, self.password)
            server.sendmail(self.login, receiver_email, message)
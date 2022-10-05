from Services.Ftp.FtpConnection import FtpConnection
from Services.Mail.MailConnection import MailConnection


class FileLoader:
    def __init__(self):
        mail_box = 'prices.mnk.group@gmail.com'
        mail_pass = 'hrsvhqkajsdjtyzr'
        self.ftp_host = '138.201.56.185'
        self.ftp_user = 'ph6802'
        self.ftp_pass = 'z7lIh8iv10pLRt'
        self.mail_con = MailConnection(mail_box, mail_pass)

    def download_from_mail(self, supplier, sender=None, subject=None):
        mail_id = self.mail_con.get_last_email_with_params(sender=sender, subject=subject)
        save_path = self.mail_con.get_mail_attachment(mail_id)
        ftp_con = FtpConnection(self.ftp_host, self.ftp_user, self.ftp_pass)
        ftp_con.upload_file(save_path, 'suppliers', supplier)


loader = FileLoader()
loader.download_from_mail(supplier='bronowski', sender='bronek@bronowski.pl', subject='Odbiorca 71233712 Oferta towarowa')
loader.download_from_mail(supplier='euroestcar', sender='margareta.peptenaru@euroestcar.ro', subject='STOCK EEC')
loader.download_from_mail(supplier='vanking', sender='raporty@vanking.com.pl')
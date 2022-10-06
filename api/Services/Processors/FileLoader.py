from Services.Ftp.FtpConnection import FtpConnection
from Services.Mail.MailConnection import MailConnection
from Services.Url.UrlConnection import UrlConnection


class FileLoader:
    def __init__(self):
        mail_box = 'prices.mnk.group@gmail.com'
        mail_pass = 'hrsvhqkajsdjtyzr'
        self.ftp_host = '138.201.56.185'
        self.ftp_user = 'ph6802'
        self.ftp_pass = 'z7lIh8iv10pLRt'
        self.mail_con = MailConnection(mail_box, mail_pass)

    def download_from_mail(self, supplier, file_name, sender=None, subject=None):
        mail_id = self.mail_con.get_last_email_with_params(sender=sender, subject=subject)
        save_path = self.mail_con.get_mail_attachment(supplier, mail_id, file_name)
        print(save_path)
        ftp_con = FtpConnection(self.ftp_host, self.ftp_user, self.ftp_pass)
        ftp_con.upload_file(save_path, 'suppliers', supplier)

    def download_from_url(self, supplier, file_name, url):
        save_path = UrlConnection.get_file(supplier, url, file_name)
        print(save_path)
        ftp_con = FtpConnection(self.ftp_host, self.ftp_user, self.ftp_pass)
        ftp_con.upload_file(save_path, 'suppliers', supplier)

    def download(self, download_type, supplier, file_name, params):
        if download_type == 'mail':
            self.download_from_mail(supplier, file_name, sender=params['sender'], subject=params['subject'])
        elif download_type == 'url':
            self.download_from_url(supplier, file_name, url=params['url'])


loader = FileLoader()

loader.download('mail', supplier='bronowski', file_name='bronowski_data.xls',
                params={'sender': 'bronek@bronowski.pl', 'subject': 'Odbiorca 71233712 Oferta towarowa'})
loader.download('mail', supplier='euroestcar', file_name='euroestcar_data.xlsx',
                params={'sender': 'margareta.peptenaru@euroestcar.ro', 'subject': 'STOCK EEC'})
loader.download('mail', supplier='vanking', file_name='vanking_data.xlsx',
                params={'sender': 'raporty@vanking.com.pl', 'subject': None})
loader.download('url', supplier='direct_24', file_name='direct_24.zip',
                params={'url': 'https://direct24.com.ua/exporter/files/d0553d0b7205c12be91588a0d134574cc364771c'})
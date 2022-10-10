from Services.Ftp.FtpConnection import FtpConnection
from Services.Loader.MailLoader import MailLoader
from Services.Loader.UrlLoader import UrlLoader


class LoadController:
    def __init__(self, ftp_auth, email_auth):
        mail_box = email_auth['address']
        mail_pass = email_auth['app_password']
        self.ftp_host = ftp_auth['host']
        self.ftp_user = ftp_auth['user']
        self.ftp_pass = ftp_auth['password']
        self.mail_con = MailLoader(mail_box, mail_pass)

    def download_from_mail(self, supplier, file_name, sender=None, subject=None):
        mail_id = self.mail_con.get_last_email_with_params(sender=sender, subject=subject)
        save_path = self.mail_con.get_mail_attachment(supplier, mail_id, file_name)
        print(save_path)
        ftp_con = FtpConnection(self.ftp_host, self.ftp_user, self.ftp_pass)
        ftp_con.upload_file(save_path, 'suppliers', supplier)

    def download_from_url(self, supplier, file_name, url):
        save_path = UrlLoader.get_file(supplier, url, file_name)
        print(save_path)
        ftp_con = FtpConnection(self.ftp_host, self.ftp_user, self.ftp_pass)
        ftp_con.upload_file(save_path, 'suppliers', supplier)

    def download(self, download_type, supplier, file_name, params):
        loader = LoadController()
        if download_type == 'mail':
            loader.download_from_mail(supplier, file_name, sender=params['sender'], subject=params['subject'])
        elif download_type == 'url':
            loader.download_from_url(supplier, file_name, url=params['url'])

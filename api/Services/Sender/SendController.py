from Services.Sender.DbSender import DbSender
from Services.Sender.FtpSender import FtpSender
from Services.load_config import Config
from Services.Generators.GeneratorController import GeneratorController

class SendController:
    @staticmethod
    def send_all():
        config = Config()
        suppliers = config.get_app_suppliers()
        for supplier in suppliers:
            print(f'sending supplier {supplier}')
            df = GeneratorController.process_supplier(supplier)
            if df is not None:
                DbSender.send(supplier, df)
                FtpSender.send(supplier)
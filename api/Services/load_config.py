import os
import io
from time import time
import yaml
import shutil
from datetime import date, time, datetime
from Utils.consts import CONFIG, CONSOLE_COLOR


def check_supplier_status(status):
    if status == True:
        return 'Enabled'
    else:
        return 'Disabled'


class Config:
    def __init__(self):
        self.config_data = ''
        with open(CONFIG.CONFIG_LOCATION+CONFIG.CONFIG_NAME, 'r') as stream:
            self.config_data = yaml.safe_load(stream)

    def get_app_info(self):
        app_version = self.config_data.get('version', 'undefined version')
        app_build = self.config_data.get('build', 'undefined build')
        return [app_build, app_version]

    def get_app_suppliers(self):
        return list(self.config_data.get('suppliers').keys())

    def get_supplier_params(self, supplier_name):
        return self.config_data.get('suppliers').get(supplier_name)

    def get_app_service_auth(self, ftp_name, email_name):
        service_dict = self.config_data.get('services_auth')

        ftp_auth = service_dict.get('ftp').get(ftp_name)
        email_auth = service_dict.get('email').get(email_name)
        return [ftp_auth, email_auth]

    def backup_config(self):
        backup_path = CONFIG.CONFIG_LOCATION + \
            f'backup/{datetime.timestamp(datetime.now())}/'
        isExist = os.path.exists(backup_path)
        if not isExist:
            os.makedirs(backup_path)
        config_backup = f'{backup_path}/{CONFIG.CONFIG_NAME}'
        shutil.copy(CONFIG.CONFIG_LOCATION+CONFIG.CONFIG_NAME, config_backup)
        print(f'{CONSOLE_COLOR.WARNING}!!! YOUR CONFIG BACKUP WAS CREATED AND IS LOCATED IN {CONSOLE_COLOR.HEADER}{config_backup}{CONSOLE_COLOR.WARNING} !!!{CONSOLE_COLOR.NC}')



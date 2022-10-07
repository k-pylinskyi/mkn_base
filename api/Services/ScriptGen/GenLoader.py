from Services.load_config import Config
from Services.Loader.LoadController import LoadController


class GenLoader:
    def __init__(self):
        self.config = Config()

        self.suppliers_list = []

    def suppliers_list_loader(self):
        self.suppliers_list = self.config.get_app_suppliers()
        active_suppliers = []
        for supplier in self.suppliers_list.items():
            if supplier[1]['status']:
                if supplier[1]['download_files']:
                    loader = LoadController()
                    print(f"{supplier[1]['download_type']} {supplier[1]['name']} {supplier[1]['download_file_name']} {supplier[1]['download_params']}")
                    loader.download(download_type=supplier[1]['download_type'],
                                    supplier=supplier[1]['name'],
                                    params=supplier[1]['download_params'],
                                    file_name=supplier[1]['download_file_name'])
                active_suppliers.append(supplier)

        return active_suppliers

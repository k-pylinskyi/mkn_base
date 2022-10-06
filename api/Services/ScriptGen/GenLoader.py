from Services.load_config import Config


class GenLoader:
    def __init__(self):
        self.config = Config()

        self.suppliers_list = []

    def suppliers_list_loader(self):
        self.suppliers_list = self.config.get_app_suppliers()
        active_suppliers = []
        for supplier in self.suppliers_list.items():
            if supplier[1]['status'] == True:

                active_suppliers.append(supplier)
        return active_suppliers

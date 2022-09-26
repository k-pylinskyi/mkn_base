# Отче наш, сущий на небесах!
# Да святится имя Твое;
# Да приидет Царствие Твое;
# Да будет воля Твоя и на земле, как на небе; 
# Хлеб наш насущный дай нам на сей день; 
# И прости нам долги наши, как и мы прощаем должникам нашим;
# И не введи нас в искушение, но избавь нас от лукавого. 
# Ибо Твое есть Царство и сила и слава вовеки.
# Аминь.
import pandas as pd


class Orap():
    def __init__(self):
        tmp_cols = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}
        location = './TemporaryStorage/ORAP/files/'
        orap_nissan_loc = location + 'orap_nissan.txt'
        orap_price_bmwall_loc = location + 'orap_price_bmwall.txt'
        orap_price_febi_blueprint_loc = location + 'orap_price_febi_blueprint.txt'
        orap_price_fiat_chrysler_loc = location + 'orap_price_fiat_chrysler.txt'
        orap_price_fiat_chrysler_l_loc = location + 'orap_price_fiat_chrysler_l.txt'

        self.orap_nissan = pd.read_csv(orap_nissan_loc, encoding_errors='ignore', sep='\t', header=None,
                                       low_memory=False, error_bad_lines=False)
        self.orap_price_bmwall = pd.read_csv(orap_price_bmwall_loc, encoding_errors='ignore', sep='\t', header=None,
                                             low_memory=False)
        self.orap_price_febi_blueprint = pd.read_csv(orap_price_febi_blueprint_loc, encoding_errors='ignore', sep='\t',
                                                     header=None, low_memory=False)
        self.orap_price_fiat_chrysler = pd.read_csv(orap_price_fiat_chrysler_loc, encoding_errors='ignore', sep='\t',
                                                    header=None, low_memory=False)
        self.orap_price_fiat_chrysler_l = pd.read_csv(orap_price_fiat_chrysler_l_loc, encoding_errors='ignore',
                                                      sep='\t', header=None, low_memory=False)

    def process(self):
        print(self.orap_nissan)
        print(self.orap_price_bmwall)
        print(self.orap_price_febi_blueprint)
        print(self.orap_price_fiat_chrysler)
        print(self.orap_price_fiat_chrysler_l)


def process_orap():
    orap = Orap()
    orap.process()


process_orap()

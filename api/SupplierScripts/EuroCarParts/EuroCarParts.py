import pandas as pd
from api.SupplierScripts import *


def euro_car_parts_to_db():
    table_name = 'euro_car_parts'
    print('Pushing {} to Data Base'.format(table_name))
    dict = get_euro_car_parts()
    for el in dict:
        DataFrameReader.dataframe_to_db_multi(el, dict[el], table_name)


def get_euro_car_parts():
    euro_car_parts = Euro_Car_Parts()
    dataframes = euro_car_parts.process()
    dict = {"bmw": dataframes[0], "hyndai": dataframes[1], "mitsubishi": dataframes[2],
            "nissan": dataframes[3], "suzuki": dataframes[4], "toyota": dataframes[5]}
    for ele in dict.keys():
        el = dict[ele]
        query = f'''
            SELECT
                el.part_number,
                el.part_number AS supplier_part_number,
                "{ele}" AS manufacturer,
                10 AS delivery,
                "PLN" AS currency,
                999 AS quantity,
                el.price,
                el.stock
            FROM 
                el 
            '''
        dict[ele] = sqldf(query)
    return dict


class Euro_Car_Parts:

    def __init__(self):
        self.bmw_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        self.hyndai_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        self.mitsubishi_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        self.nissan_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        self.suzuki_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        self.toyota_columns = {
            0: 'part_number',
            1: 'price',
            2: 'stock'
        }

        bmw_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/BMW" \
                  "/BMW_MNKGroupSpzoo2022122011254463a17f9891ff4.zip "
        hyndai_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/Hundai" \
                     "/HYUNDAI_MNKGroupSpzoo2022122011255363a17fa1ba7a8.zip "
        mitsubishi_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/Mitsubishi" \
                         "/MITSUBISHI_MNKGroupSpzoo2022122011255563a17fa376314.zip "
        nissan_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/Nissan" \
                     "/NISSAN_MNKGroupSpzoo2022122011255663a17fa4b19eb.zip "
        suzuki_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/Suzuki" \
                     "/SUZUKI_MNKGroupSpzoo2022122011255763a17fa5e84ae.zip "
        toyota_url = "ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/Euro_Car_Parts/Toyota" \
                     "/TOYOTA_MNKGroupSpzoo2022122011260063a17fa8ebaa4.zip "

        self.bmw = pd.read_csv(bmw_url, sep=',', header=None, encoding_errors='ignore',
                               compression='zip', low_memory=False)
        self.hyndai = pd.read_csv(hyndai_url, sep=',', header=None, encoding_errors='ignore',
                                  compression='zip', low_memory=False)
        self.mitsubishi = pd.read_csv(mitsubishi_url, sep=',', header=None, encoding_errors='ignore',
                                      compression='zip', low_memory=False)
        self.nissan = pd.read_csv(nissan_url, sep=',', header=None, encoding_errors='ignore',
                                  compression='zip', low_memory=False)
        self.suzuki = pd.read_csv(suzuki_url, sep=',', header=None, encoding_errors='ignore',
                                  compression='zip', low_memory=False)
        self.toyota = pd.read_csv(toyota_url, sep=',', header=None, encoding_errors='ignore',
                                  compression='zip', low_memory=False)

    def process(self):
        self.bmw.rename(columns=self.bmw_columns, inplace=True)
        self.hyndai.rename(columns=self.hyndai_columns, inplace=True)
        self.mitsubishi.rename(columns=self.mitsubishi_columns, inplace=True)
        self.nissan.rename(columns=self.nissan_columns, inplace=True)
        self.suzuki.rename(columns=self.suzuki_columns, inplace=True)
        self.toyota.rename(columns=self.toyota_columns, inplace=True)
        
        return [self.bmw, self.hyndai, self.mitsubishi, self.nissan, self.suzuki, self.toyota]

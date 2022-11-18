import os.path

from Services.Processors.DataFrameReader import *
import pandas as pd
import requests


def direct24_to_db():
    table_name = 'direct24'
    print('Pushing {} to Data Base'.format(table_name))
    DataFrameReader.dataframe_to_db(table_name, get_direct24_data())


def get_direct24_data():
    direct = Direct24()
    dataframes = direct.process()
    data = dataframes
    data[['day_1', 'day_2']] = data['delivery'].str.split('-', expand=True)
    data['day_1'] = pd.to_numeric(data['day_1'])
    data['day_2'] = pd.to_numeric(data['day_2'])
    data['quantity'] = data['quantity'].str.replace('>', '')
    data['part_number'] = data['supplier_part_number']

    data = data[data['day_2'] <= 8]

    data = data.dropna()

    return data


def get_file():
    # Fill in your details here to be posted to the login form.
    payload = {
        'username': 'aroza@ua.fm',
        'password': '197824197824'
    }

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        p = s.post('https://direct24.com.ua/users/login/?next=/', data=payload)
        # print the html returned or something more intelligent to see if it's a successful login page.
        # print(p.text)

        # An authorised request.
        resp = s.get('https://direct24.com.ua/exporter/files/531f50598d684d387912e8e974c5d78965212657/')
        save_folder = '../TemporaryStorage/direct24'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_path = os.path.join(save_folder, 'direct24.zip')

        with open(save_path, 'wb') as f:
            f.write(resp.content)

        return save_path


class Direct24:
    def __init__(self):
        data = get_file()
        self.data_columns = {
            0: 'manufacturer',
            1: 'supplier_part_number',
            2: 'part_name',
            3: 'quantity',
            4: 'price',
            5: 'delivery'
        }

        self.data = pd.read_csv(data, encoding_errors='ignore', usecols=[0, 1, 2, 3, 4, 5], header=None,
                                sep=';', on_bad_lines='skip', skiprows=2, low_memory=False, decimal=',')

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)
        return self.data


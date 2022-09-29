from api.SupplierScripts import *


def inter_team_to_db():
    print('Pushing Inter Team to Data Base')
    DataFrameReader.dataframe_to_db('inter_team', get_inter_team_data())


def get_inter_team_data():
    inter_team = InterTeam()
    data = inter_team.process()

    query = '''
        SELECT
            26 as supplier_id,
            manufacturer,
            part_number as supplier_part_number,
            part_number,
            price + deposit as price,
            qty_1 + qty_2 as quantity
        FROM 
            data  
    '''

    return sqldf(query)


class InterTeam:
    def __init__(self):
        self.data_columns = {
            0: 'part_number',
            1: 'part_name',
            2: 'qty_1',
            3: 'qty_2',
            4: 'price',
            5: 'manufacturer',
            6: 'deposit'
        }

        self.data = pd.read_csv(
            '../TemporaryStorage/INTER_TEAM//files//interteam_data.csv',
            sep=';', encoding_errors='ignore', header=None, skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6])

    def process(self):
        self.data.rename(columns=self.data_columns, inplace=True)

        return self.data

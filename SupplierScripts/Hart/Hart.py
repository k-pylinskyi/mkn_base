from SupplierScripts.DataFrameReader import DataFrameReader as dfreader
import pandasql as pdsql

class Hart:
    def __init__(self):
        directory = "./TemporaryStorage//Hart//files"
        dfs_dict = dfreader.get_data_frames(directory)

    def process(self):
        pass

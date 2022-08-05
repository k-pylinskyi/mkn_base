from Services.DbService import *

class DownloadProcessor:
    def __init__(self):
        db = DbService()

        rows = db.select('select_supliers.sql')

        print(rows)
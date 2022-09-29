from threading import Thread, active_count
from api.Utils.consts import CONSOLE_COLOR, PATHS, ERRORS
from api.Services.Db.DbService import DbService
from api.Services.Ftp.FtpConection import FtpConnection
from api.SupplierScripts.Hart.Hart import *
from api.SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import *
from api.SupplierScripts.Emoto.Emoto import *
from api.SupplierScripts.Gordon.Gordon import *
from api.SupplierScripts.Motorol.Motorol import *
from api.SupplierScripts.Paketo.Paketo import *
from api.SupplierScripts.Rodon.Rodon import *
from api.SupplierScripts.Motogama.Motogama import *
from api.SupplierScripts.Elit.Elit import *

db = DbService()


def suppliers_to_db():

    print('Starting pushing to Data Base')

    autopartner_gdansk_to_db()
    emoto_to_db()
    gordon_to_db()
    motorol_to_db()
    paketo_to_db()
    hart_to_db()
    rodon_to_db()
    motogama_to_db()
    elit_to_db()

    print('Dataframes pushed to Data Base')

    print('Creating View Tables')
    db.create_views()
    print('Views created')


def suppliers_to_ftp():
    suppliers = [
        'auto_partner_gdansk',
        'emoto',
        'gordon',
        'motorol',
        'paketo',
        'hart',
        'rodon',
        'motogama',
        'elit'
    ]

    for supplier in suppliers:
        print('Exporting {} to csv'.format(supplier))
        file = db.get_table_csv(supplier)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_file(file, supplier)



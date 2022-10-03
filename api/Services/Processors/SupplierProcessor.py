from threading import Thread, active_count
from api.Utils.consts import CONSOLE_COLOR, PATHS, ERRORS
from Services.Db.DbService import DbService
from Services.Ftp.FtpConection import FtpConnection
from SupplierScripts.Hart.Hart import *
from SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import *
from SupplierScripts.Emoto.Emoto import *
from SupplierScripts.Gordon.Gordon import *
from SupplierScripts.Motorol.Motorol import *
from SupplierScripts.Paketo.Paketo import *
from SupplierScripts.Rodon.Rodon import *
from SupplierScripts.Motogama.Motogama import *
from SupplierScripts.Elit.Elit import *
from SupplierScripts.InterTeam.InterTeam import *
from SupplierScripts.AutoLand.AutoLand import *
from SupplierScripts.Motoprofil.Motoprofil import *
from SupplierScripts.Intervito.Intervito import *
from SupplierScripts.KrisAuto.KrisAuto import *

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
    inter_team_to_db()
    autoland_to_db()
    motorol_to_db()
    motoprofil_to_db()
    krisauto_to_db()
    intervito_to_db()

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
        'elit',
        'inter_team',
        'autoland',
        'motoprofil',
        'krisauto',
        'intervito'
    ]
    for supplier in suppliers:
        print('Exporting {} to csv'.format(supplier))
        file = db.get_table_csv(supplier)
        ftp = FtpConnection('138.201.56.185', 'ph6802', 'z7lIh8iv10pLRt')
        ftp.upload_file(file, supplier)



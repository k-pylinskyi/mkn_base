from threading import Thread, active_count
from api.Utils.consts import CONSOLE_COLOR, PATHS, ERRORS
from api.Services.Db import DbService
from api.SupplierScripts.Hart.Hart import *
from api.SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import *
from api.SupplierScripts.Emoto.Emoto import *
from api.SupplierScripts.Gordon.Gordon import *
from api.SupplierScripts.Motorol.Motorol import *
from api.SupplierScripts.Paketo.Paketo import *


def suppliers_to_db():

    print('Starting pushing to Data Base')
    #autopartner_gdansk_to_db()
    #emoto_to_db()
    #gordon_to_db()
    #motorol_to_db()
    #paketo_to_db()
    #hart_to_db()
    print('Dataframes pushed to Data Base')

    print('Creating View Tables')
    DbService.create_views()
    print('Views created')





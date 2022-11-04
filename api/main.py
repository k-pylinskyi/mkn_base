from Services.Sender.SendController import SendController
from SupplierScripts.Hart.Hart import *
from SupplierScripts.Autopartner.Autopartner import *
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
from SupplierScripts.Direct24.Direct24 import *
from SupplierScripts.Bronowski.Bronowski import *
from SupplierScripts.Vanking.Vanking import vanking_to_db
from Services.Loader.LoadController import LoadController
from Services.load_config import Config

if __name__ == '__main__':
    config = Config()
    auth = config.get_app_service_auth('main', 'main')
    loader = LoadController(auth[0], auth[1])
    loader.download('mail', 'euro_est_car', 'euro_est_car.xlsx',
                    params={'sender': 'margareta.peptenaru@euroestcar.ro', 'subject': 'STOCK EEC'})
    vanking_to_db()
    bronowski_to_db()
    direct24_to_db()
    intervito_to_db()
    autopartner_to_db()
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

    # SendController.send_all()
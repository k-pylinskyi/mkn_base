from flask import Flask
from SupplierScripts.Paketo.Packeto import process_paketo
from SupplierScripts.AutopartnerGdansk.AutopartnerGdansk import process_autopartner_gdansk

app = Flask(__name__)


@app.route('/suppliers/<supplier>')
def supplier_details(supplier):
        if (supplier == 'paketo'):
            return {'data': process_paketo()}
        elif (supplier == 'autopartner_gdansk'):
            return {'data': process_autopartner_gdansk()}
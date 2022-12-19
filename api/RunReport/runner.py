from __init__ import *
from Services.Email.EmailSender import EmailSender
from RunReport.MaxiChecker import login_maxi, check_manager
from RunReport.FTPChecker import ftp_connect
from RunReport.FTPChecker import check_files
import datetime
from SupplierScripts.Toyota_Warszawa_Wola.Toyota_Warszawa_Wola import toyota_warszawa_wola_to_db


funcs = [
    # (toyota_warszawa_wola_to_db, {'M Toyota Warszawa Wola CCC': ['M Toyota Warszawa Wola EXP']}),
    (autofrance_to_db, {'M AUTO-FRANCE': ['Auto france']}),
    (ronax_to_db, {'M Ronax': ['RONAX VAG', 'RONAX BMW', 'RONAX TOYOTA', 'RONAX RENAULT']}),
    (autopartner_to_db, {'M Auto Partner': ['Auto Partner EXP']}),
    # (voyagerGroup_to_db, {'M Voyager Group': ['VOYAGER MAZDA']}),
    # (autoland_to_db, {'M Auto Land': ['Auto Land']}),
    # intercars_to_db,
    # autofusbmw_to_db,
    # autoeuro_to_db,
    # hart_to_db,
    # zdunek_to_db,
    # euroestcar_to_db,
    # vanking_to_db,
    # bronowski_to_db,
    # direct24_to_db,
    # intervito_to_db,
    # autopartner_gdansk_to_db,
    # emoto_to_db,
    # gordon_to_db,
    # motorol_to_db,
    # paketo_to_db,
    # rodon_to_db,
    # motogama_to_db,
    # elit_to_db,
    # inter_team_to_db,
    # motorol_to_db,
    # motoprofil_to_db,
    # krisauto_to_db,
    # DbService.get_db_backup
]


class Runner:
    @staticmethod
    def run():
        sender = EmailSender()
        driver = login_maxi()

        start_total = datetime.datetime.now()
        html = '''
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            .styled-table {
                border-collapse: collapse;
                margin: 25px 0;
                font-size: 0.9em;
                font-family: sans-serif;
                min-width: 400px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            }
            .active {
                background-color: #6ff29b;
            }
            .notactive {
                background-color: #f77272;
            }
            .styled-table thead tr {
                background-color: #009879;
                color: #ffffff;
                text-align: left;
            }
            .styled-table th,
            .styled-table td {
                padding: 12px 15px;
            }
            .styled-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            
            .styled-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            
            .styled-table tbody tr:last-of-type {
                border-bottom: 2px solid #009879;
            }
            
            .styled-table tbody tr.active-row {
                font-weight: bold;
                color: #009879;
            }
            </style>
            </head>
            <body>
            <h2>Updating Report</h2>
            <table class="styled-table">
                <tr>
                    <th>Supplier</th>
                    <th>Report</th>
                    <th>Took</th>
                    <th>Load/Supplier</th>
                    <th>File UPD</th>
                    <th>DB UPD</th>
                    <th>Status </th>
                </tr>
        '''
        suppliers_cnt = 0

        for f in funcs:
            try:
                suppliers_cnt = suppliers_cnt + 1
                func = f[0]
                print(f'starting {func.__name__}')
                start = datetime.datetime.now()
                ftp_cred = func()
                load, supplier, file_upd, db_upd, active = list(map(list, zip(*check_manager(f[1], driver))))
                check_files(ftp_cred)
                end = datetime.datetime.now()
                print(f'func {func.__name__} took {end - start}')
                for index, el in enumerate(load):
                    html = f'{html}<tr>'
                    html = f'{html}<td>{func.__name__.replace("_to_db", "").upper()}</td>'
                    html = f'{html}<td>Updated</td>'
                    html = f'{html}<td>{end - start}</td>'

                    html = f'{html}<td>{el}</td>'
                    html = f'{html}<td>{file_upd[index]}</td>'
                    html = f'{html}<td>{db_upd[index]}</td>'
                    if active[index] == "activated":
                        html = f'{html}<td class="active">{active[index]}</td>'
                    html = f'{html}</tr>'
            except Exception as ex:
                print(f'Error occurred:n{ex}')
                html = f'{html}<tr>\n'
                html = f'{html}<td>{func.__name__.replace("_to_db", "").upper()}</td>\n'
                html = f'{html}<td>Error occurred</td>\n'
                html = f'{html}<td>0</td>\n'

                html = f'{html}<td>0</td>'
                html = f'{html}<td>0</td>'
                html = f'{html}<td>0</td>'
                html = f'{html}<td>0</td>'
                html = f'{html}</tr>\n'
        end_total = datetime.datetime.now()
        html = f'{html}</table>\n'
        html = f'{html}<p>Database update took <b>{end_total - start_total}</b></p>'
        html = f'{html}<p>Total suppliers <b>{suppliers_cnt}</b></p>'
        html = f'{html}</body></html>'
        sender.send(html)
        print(f'database update took {end_total - start_total}')

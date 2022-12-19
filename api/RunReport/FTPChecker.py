from datetime import timedelta
from ftplib import FTP
from dateutil import parser

from Services.Ftp.FtpConnection import FtpConnection


def parse_ftp(object):
    ftp_list = [[attribute, value] for attribute, value in object.__dict__.items() if 'ftp' in value]
    cred_list = []
    for el in ftp_list:
        # 'ftp://ph6802:z7lIh8iv10pLRt@138.201.56.185/suppliers/voyager_group/voyager_3_days.csv'
        attr, value = el
        cred = value.split('/')[2]
        path = value.replace(cred, '').replace('ftp://', '')
        lp, ip = cred.split('@')
        login, passw = lp.split(':')

        # print(f'ip: {ip}\n'
        #       f'login: {login}\n'
        #       f'pass: {passw}\n'
        #       f'path: {path}')
        cred_list.append([ip, login, passw, path])
    return cred_list


def ftp_connect(host, username, password):
    ftp = FTP(host)  # connect to host, default port

    ftp.login(user=username, passwd=password)
    return ftp


def check_files(cred_list):
    print('==========================')
    for el in cred_list:
        ftp = ftp_connect(el[0], el[1], el[2])
        path_spl = el[3].split("/")
        dir = f'/{path_spl[1]}/{path_spl[2]}'
        file = path_spl[3]
        ftp.cwd(dir)
        myList = list(ftp.mlsd(path="", facts=["name", "modify"]))
        for item in myList:
            if item[0] == file:
                print(f'{file}: {(parser.parse(item[1]["modify"])) + timedelta(hours=1)}')
    print('==========================')

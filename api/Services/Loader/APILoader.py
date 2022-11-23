import os
import urllib.request
import zipfile

import requests


def downloadFileFromAPI(url_dict):
    # url_dict form
    # url_dict = {'baseurl': 'https://data.webapi.intercars.eu/customer/99FIIU/Stock/Stock_2022-11-21.csv.zip',
    #             'supplier_name': 'intercars', 'payload': ('FjAqKSFg7j6NwSf8', '99FIIU'), 'zip': True}
    baseurl = url_dict['baseurl']
    payload = url_dict['payload']
    supplier_name = url_dict['supplier_name']
    zip = url_dict['zip']

    file_name = '/' + baseurl.split('/')[-1]
    absolute_path = pathCreator('\\' + supplier_name)
    password, username = payload

    manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, baseurl, username, password)
    auth = urllib.request.HTTPBasicAuthHandler(manager)
    opener = urllib.request.build_opener(auth)
    urllib.request.install_opener(opener)

    response = urllib.request.urlopen(baseurl)

    f = open(absolute_path + file_name, 'wb')
    f.write(response.read())

    print(f'Downloaded file {file_name}')

    if zip:
        unzip(absolute_path, file_name)

    return absolute_path


def pathCreator(folder_name):
    print(folder_name)
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    os.chdir('TemporaryStorage')
    absolute_path = os.getcwd() + folder_name

    if not os.path.exists(folder_name[1:]):
        os.makedirs(folder_name[1:])
        print(f"{folder_name} directory created")
    else:
        print(f"{folder_name} directory exists")
    return absolute_path


def unzip(absolute_path, file_name):
    with zipfile.ZipFile(absolute_path + file_name, 'r') as zip_ref:
        zip_ref.extractall(absolute_path)

import os
import urllib.request
import zipfile
from datetime import date, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import *
from bs4 import BeautifulSoup
import dateutil.parser as dparser


def fileDate(url_dict):
    baseurl = url_dict['baseurl']
    payload = url_dict['payload']
    password, username = payload

    manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    connCreate(baseurl, username, password, manager)
    response = urllib.request.urlopen(baseurl).read()

    soup = BeautifulSoup(response, 'html.parser')
    x = (soup.find_all('a'))
    dates = {}
    for i in x:
        file_name = i.extract().get_text()
        url_new = baseurl + file_name
        url_new = url_new.replace(" ", "%20")
        if file_name[-1] == '/' and file_name[0] != '.':
            url_dict['baseurl'] = url_new
            fileDate(url_dict)
        if 'csv.zip' in url_new:
            file_name = url_new.replace(baseurl, '')
            dates[file_name] = dateFromString(file_name)
            print(f'{file_name} | {dates[file_name]}')

    return dates


def downloadFileFromAPI(url_dict):
    # url_dict form
    # url_dict = {'baseurl': 'https://data.webapi.intercars.eu/customer/99FIIU/Stock/Stock_2022-11-21.csv.zip',
    #             'supplier_name': 'intercars', 'payload': ('FjAqKSFg7j6NwSf8', '99FIIU'), 'zip': True}

    baseurl = url_dict['baseurl']
    payload = url_dict['payload']
    supplier_name = url_dict['supplier_name']
    zip = url_dict['zip']
    password, username = payload

    manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    connCreate(baseurl, username, password, manager)

    file_name = '/' + baseurl.split('/')[-1]
    absolute_path = pathCreator('\\' + supplier_name)

    response = urllib.request.urlopen(baseurl)

    # try:
    #     response = urllib.request.urlopen(baseurl)
    #     date_ = date.today().strftime("%Y-%m-%d")
    # except HTTPError as e:
    #     if e.code == 404 and supplier_name == 'intercars':
    #         date_ = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    #
    #         baseurl = f'{baseurl[:-18]}{date_}.csv.zip'
    #         file_name = '/' + baseurl.split('/')[-1]
    #
    #         connCreate(baseurl, username, password, manager)
    #
    #         response = urllib.request.urlopen(baseurl)

    f = open(absolute_path + file_name, 'wb')
    f.write(response.read())

    print(f'Downloaded file {baseurl}')

    if zip:
        unzip(absolute_path, file_name)


def pathCreator(folder_name):
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


def newestFile(dates):
    return max(dates)


def dateFromString(file_name):
    date = dparser.parse(file_name, fuzzy=True).strftime('%Y-%m-%d')
    return date


def connCreate(baseurl, username, password, manager):
    manager.add_password(None, baseurl, username, password)
    auth = urllib.request.HTTPBasicAuthHandler(manager)
    opener = urllib.request.build_opener(auth)
    urllib.request.install_opener(opener)


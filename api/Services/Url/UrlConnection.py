import requests as req
from urllib.request import urlopen
import shutil
from contextlib import closing


def get_file_from_request(url, save_path):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    resp = req.get(url, headers=user_agent)
    with open(save_path, 'wb') as f:
        f.write(resp.content)


def get_file_from_url(url, save_path):
    with closing(urlopen(url)) as r:
        with open(save_path, 'wb') as f:
            shutil.copyfileobj(r, f)


class UrlConnection:
    @staticmethod
    def get_file(url, save_path):
        if url.lower().startswith('ftp://'):
            try:
                print(f'Getting file from FTP URL: {url}')
                get_file_from_url(url, save_path)
            except Exception as ex:
                print(f'Exception occurred while getting file!\nURL: {url}\nException: {ex}')
        else:
            try:
                print(f'Getting file with Request: {url}')
                get_file_from_request(url, save_path)
            except Exception as ex:
                print(f'Exception occurred while getting file!\nRequest: {url}\nException: {ex}')


UrlConnection.get_file('https://sun9-83.userapi.com/impg/V5U4N2Y2e-pmlhcxtuyeY0BcYHVTwSdS0ibcVA/8djQwfVlwGo.jpg?size=360x270&quality=96&sign=fa565523c28bd5cf31c1d6adf01cca37&type=album', 'some.jpg')
UrlConnection.get_file('ftp://hart:2Y1r7D0g@138.201.56.185/hart.zip', 'hart.zip')
UrlConnection.get_file('https://direct24.com.ua/exporter/files/d0553d0b7205c12be91588a0d134574cc364771c', 'direct24.zip')
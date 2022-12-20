import math
import datetime

import pandas as pd
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from Services.Db.DbContext import DbRatesContext
from Services.Processors.DataFrameReader import DataFrameReader

LOGIN_URL = "https://www.maxi.parts/admin/login/"
RATE_URL = 'https://www.maxi.parts/admin/eshop/settings/rates.html?subj=EditTable_Form1&fn=add'
UAH_RATE_URL = 'https://obmennovosti.info/city.php?city=42'
CLIENT_RATE_URL = 'https://www.maxi.parts/admin/content/structure3.0.html?str_id=808&fn=edit'
DRIVER_PATH = r'C:\Users\admino4ka\Documents/chromedriver.exe'
LOGIN = 'nikitak_k'
PASSWORD = '3sw3ar'


def rate_update_manager():
    driver = login_maxi()
    rates_source = rate_request(driver)
    rate_dict = rate_calc(rates_source)
    print(rate_dict)
    # for key in rate_dict.keys():
    #     update_rate(key, rate_dict[key], driver)
    # update_client_uah(driver, rates_source["uah"])

    # take_screenshot(driver)
    # telegram_bot([f'rates_client_text_{datetime.date.today()}.png', f'rates_{datetime.date.today()}.png'])


def login_maxi():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(LOGIN_URL)

    login_field = driver.find_element(By.NAME, "Login[username]")
    pass_field = driver.find_element(By.NAME, "Login[password]")
    login_button = driver.find_element(By.CLASS_NAME, "btn_accent")

    login_field.send_keys(LOGIN)
    sleep(0.5)
    pass_field.send_keys(PASSWORD)
    sleep(0.5)
    login_button.click()
    sleep(1)
    if driver.title != 'Authorization':
        print('Successfully logged in')
    else:
        print('Incorrect login/password')
    sleep(1)
    return driver


def rate_request(driver):
    rate_tmp = {"2": "usd", "3": "uah", "9": "gbp", "eur": "eur"}
    rate_source = {}
    today = datetime.date.today()
    if str(today.weekday()) == "0":
        today = today - datetime.timedelta(days=3)
    elif str(today.weekday()) != "0":
        today = today - datetime.timedelta(days=1)

    today_str = datetime.datetime.strftime(today, "%Y-%m-%d")
    for el in rate_tmp.values():
        x = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/a/{el}/{today_str}/')
        if int(x.status_code) == 200:
            rate = round_decimals_up(x.json()["rates"][0]["mid"])
        else:
            rate = -1

        rate_source[el] = rate
    rate_source['uah'] = uah_parser(driver)
    print(rate_source)
    return rate_source


def update_rate(RATE_NUM, RATE_VALUE, driver):
    driver.get(RATE_URL)

    select = Select(driver.find_element(By.NAME, 'crt_target_cur_id'))

    select.select_by_value(RATE_NUM)
    rate_value = driver.find_element(By.NAME, "crt_rate")
    submit_button = driver.find_element(By.NAME, "send")

    rate_value.send_keys(RATE_VALUE)
    submit_button.click()

    sleep(3)


def rate_calc(rates_source):
    rates_dict = {}
    usd = lambda usd_zl, eur_zl: float(usd_zl) / float(eur_zl)
    uah = lambda uah_zl: 1 / float(uah_zl)
    zl = lambda eur_zl: 1 / float(eur_zl)
    gbp = lambda gbp_zl, eur_zl: float(gbp_zl) / float(eur_zl)

    rates_dict["2"] = round(usd(rates_source["usd"], rates_source["eur"]), 6)
    rates_dict["3"] = round(uah(rates_source["uah"]), 6)
    rates_dict["8"] = round(zl(rates_source["eur"]), 6)
    rates_dict["9"] = round(gbp(rates_source["gbp"], rates_source["eur"]), 6)

    return rates_dict


def round_decimals_up(number: float, decimals: int = 3):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


def uah_parser(driver):
    driver.get(UAH_RATE_URL)
    uah_euro = driver.find_element(By.XPATH,
                                   '//*[@id="app"]/main/div/div/div/div/div/div/table/tbody/tr[3]')

    rate_kp = uah_euro.text.split(' ')[1].split('/')
    # KF_rate = round_decimals_up((float(rate_kp[0]) + float(rate_kp[1])) / 2)
    KF_rate = round_decimals_up(float(rate_kp[1]))
    KF_yesterday = kf_yesterday()
    delta = round_decimals_up(((KF_rate - KF_yesterday)/KF_rate) * 100, 2)
    # print("KF_rate: " + str(KF_rate))
    # print("delta: " + str(delta))

    if delta >= 0.5:
        add_delta = 0.5
    elif delta < 0.5:
        add_delta = 0.35
    final_rate = round_decimals_up(KF_rate * (1 + add_delta/100), 2)
    print(final_rate)
    DataFrameReader.rate_to_db(KF_rate, str((datetime.date.today())).replace("-", ""))
    return final_rate


def kf_yesterday():
    date = datetime.date.today()
    KF_yesterday = receive_previous_rate(date)

    return KF_yesterday


def receive_previous_rate(today):
    date_y = today - datetime.timedelta(days=1)
    row = get_rate(date_y)
    print(f"row {row}")
    rate = row[0][0]
    return rate


def get_rate(yesterday):
    yes = str(yesterday).replace("-", "")
    context = DbRatesContext()
    connection = context.db

    table_df = pd.read_sql_query(f' SELECT rate, date_t FROM rates', connection)
    row = table_df.loc[table_df['date_t'] == yes].values.tolist()
    return row


def rate_date_uah(driver):
    value = driver.execute_script('javascript:alert(document.lastModified).value')
    alert = driver.switch_to.alert
    # print(datetime.datetime.now())
    # print(alert.text)
    alert.accept()


def take_screenshot(driver):
    driver.get('https://www.maxi.parts/admin/eshop/settings/rates.html')
    sleep(2)

    rates_table = driver.find_element(By.XPATH, "/html/body/div[1]/div/table[3]")
    rates_table.screenshot(f'rates_{datetime.date.today()}.png')


def update_client_uah(driver, uah_rate):
    cookies = {
        'admin-lng': 'ru',
        'useFileBrowser': '1',
        'PHPSESSID': '7c611211c56e49252ba0f46d52cc78f9',
        'baseUrl': '%2Fselfprice%2F',
        'mstto': 'ru',
        'force_stock_id': '7',
        'USER': 'nikitak_k%3A99ff05f0e321a6ad25a9a08b1d72b4d95e99e12c',
        'tre_pre_load58': '1',
        'tre_pre_load372': '0',
        'tre_pre_load482': '1',
        'search-show-adv-options': '0',
    }

    headers = {
        'authority': 'www.maxi.parts',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'admin-lng=ru; useFileBrowser=1;
        # PHPSESSID=7c611211c56e49252ba0f46d52cc78f9; baseUrl=%2Fselfprice%2F; mstto=ru; force_stock_id=7;
        # USER=nikitak_k%3A99ff05f0e321a6ad25a9a08b1d72b4d95e99e12c; tre_pre_load58=1; tre_pre_load372=0;
        # tre_pre_load482=1; search-show-adv-options=0',
        'origin': 'https://www.maxi.parts',
        'referer': 'https://www.maxi.parts/admin/content/structure3.0.html?str_id=808&fn=edit',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
    }

    params = {
        'str_id': '808',
        'fn': 'edit',
    }

    data = {
        'id-translate': 'YTozOntzOjk6InRhYmxlbmFtZSI7czoxODoiX29iamVjdHNfc3RydWN0dXJlIjtzOjQ6ImFyUEsiO2E6MTp7aTowO3M6Njoic3RyX2lkIjt9czo3OiJhclBLVmFsIjthOjE6e3M6Njoic3RyX2lkIjtzOjM6IjgwOCI7fX0=',
        '__str_id__': '808',
        'new_parent_id': '-1',
        'str_published': 'A',
        'str_domain': '',
        'str_lng_id': '',
        'str_interface': '_common_user',
        'str_name': 'template_bottom_header',
        'str_title': 'Текст внизу шапки сайта',
        'str_text_de': f'<p><strong>КУРС EUR/ГРН {uah_rate}</strong></p>',
        'str_text_en': f'<p><strong>КУРС EUR/ГРН {uah_rate}</strong></p>',
        'str_text_pl': f'<p><strong>КУРС EUR/ГРН {uah_rate}</strong></p>',
        'str_text_ru': f'<p><strong>КУРС EUR/ГРН {uah_rate}</strong></p>',
        'str_text_uk': f'<p><strong>КУРС EUR/ГРН {uah_rate}</strong></p>',
        'translated[]': 'str_text',
        'translated-semantic[]': 'str_text_808',
        'translated-set': 'Content',
        'str_last_modified': '',
        'str_metadata[item][]': '',
        'str_metadata[value][]': '',
        'send': 'Подача запроса',
    }

    response = requests.post(
        'https://www.maxi.parts/admin/content/structure3.0.html',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    sleep(5)
    driver.get(CLIENT_RATE_URL)
    rates_elem = driver.find_element(By.XPATH, "/html/body/form[2]/table/tbody/tr[10]/td[2]")
    rates_elem.screenshot(f'rates_client_text_{datetime.date.today()}.png')


def telegram_bot(images):
    # TOKEN = "5626443532:AAH6qUPbClJImsnpQIQ2PB_Bsk-oTAy2LBQ"
    # url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    # print(requests.get(url).json())

    TOKEN = "5626443532:AAH6qUPbClJImsnpQIQ2PB_Bsk-oTAy2LBQ"
    url = f"https://api.telegram.org/bot{TOKEN}/"
    chat_id = "161856757"
    for image in images:
        requests.post(url + 'sendPhoto', data={'chat_id': chat_id},
                      files={'photo': open(image, 'rb')})

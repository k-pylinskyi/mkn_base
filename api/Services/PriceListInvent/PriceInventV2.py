import math
import datetime

import pandas as pd
import requests
from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from Services.UpdateRate.UpdateRate import login_maxi

from Services.Logger.wrapper import timeit

PRICE_PAGE = "https://www.maxi.parts/admin/pricelists/"
PRICE_LIST_SETTINGS = "https://www.maxi.parts/admin/pricelists/?subj=EditTable_Form1&fn=edit&kmp_id="
DOWNLOAD_PREFIX = "https://www.maxi.parts"


@timeit
def vyManager():
    driver = login_maxi()
    pricePageParse(driver)


def pricePageParse(driver):
    driver.get(PRICE_PAGE)
    price_list = []
    num_rows_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[6]/div[3]/div/div[2]/a[5]")
    num_rows_button.click()
    sleep(1)
    tables = driver.find_elements(By.CLASS_NAME, "admin_edit_table")
    for elm in tables:
        if elm.get_attribute("data-id") == 'task_prices':
            table = elm
    table_t = table.find_element(By.XPATH, "./tbody")

    priceList_rows = table_t.find_elements(By.XPATH, "./tr")  # [1:10]
    price_num_list = []

    for row in priceList_rows[1:]:
        print("==================================")
        price_num = row.find_element(By.CLASS_NAME, "col_kmp_id").text
        price_num_list.append(price_num)
        link_field = row.find_element(By.CLASS_NAME, "col_file")

        try:
            file_name = link_field.find_element(By.XPATH, "./nobr/a").get_attribute("download")
        except NoSuchElementException:
            file_name = 'No file'

        try:
            file_link = str(link_field.find_element(By.XPATH, "./nobr/a").get_attribute("href"))
        except NoSuchElementException:
            file_link = 'No link'

        print("price num: " + str(price_num))
        print(f"file name: {file_name}")
        print("file link: " + str(file_link))
        price_list.append([str(price_num), str(file_name), str(file_link)])

    for index, num in enumerate(price_list):
        print(num[0])
        start = datetime.datetime.now()

        try:
            driver.get(PRICE_LIST_SETTINGS + str(num[0]))
            # SUPPLIERS
            select_box_suppliers = Select(driver.find_element(By.XPATH,
                                                              "/html/body/div[1]/div/form/table/tbody/tr[6]/td[2]/select"))
            tmp_one = []
            for ele in select_box_suppliers.all_selected_options:
                tmp_one.append(ele.text)
            suppliers = ' '.join(str(e) for e in tmp_one)
        except NoSuchElementException:
            suppliers = 'empty'

        end = datetime.datetime.now()
        print(end-start)

        # MANUFACTURERS
        # try:
        #     select_manufacturer_box = Select(driver.find_element(By.XPATH,
        #                                                          "/html/body/div[1]/div/form/table/tbody/tr[7]/td[2]/select"))
        #     tmp_two = []
        #     for ele in select_manufacturer_box.all_selected_options:
        #         tmp_two.append(ele.text)
        #     manufacturers = ' '.join(str(e) for e in tmp_two)
        # except NoSuchElementException:
        #     manufacturers = 'empty'
        #
        start = datetime.datetime.now()
        # print(start - end)

        # EMAIL/NAME
        try:
            email_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[9]/td[2]/input") \
                .get_attribute('value')
        except NoSuchElementException:
            email_box = 'No email'

        end = datetime.datetime.now()
        print(end - start)

        # CLIENT GROUP
        try:
            client_group_box = Select(driver.find_element(By.XPATH,
                                                          "/html/body/div[1]/div/form/table/tbody/tr[10]/td[2]/select"))
            for elem in client_group_box.all_selected_options:
                client_group = elem.text
        except NoSuchElementException:
            client_group = 'empty'

        start = datetime.datetime.now()
        print(start - end)

        # CLIENT CATEGORY
        try:
            group_categ_box = Select(driver.find_element(By.XPATH,
                                                         "/html/body/div[1]/div/form/table/tbody/tr[11]/td[2]/select"))
            for elem in group_categ_box.all_selected_options:
                client_categ = elem.text
        except NoSuchElementException:
            client_categ = 'empty'

        end = datetime.datetime.now()
        print(end - start)

        # COMPLEX RESTRICTiONS
        try:
            restrictions = Select(driver.find_element(By.XPATH,
                                                      "/html/body/div[1]/div/form/table/tbody/tr[19]/td[2]/select"))
            for elem in restrictions.all_selected_options:
                restriction_status = elem.text
        except NoSuchElementException:
            restriction_status = 'empty'

        start = datetime.datetime.now()
        print(start - end)

        # STRING AS FORMULA txt/csv
        try:
            str_as_formula = Select(driver.find_element(By.XPATH,
                                                        "/html/body/div[1]/div/form/table/tbody/tr[28]/td[2]/select"))
            for elem in str_as_formula.all_selected_options:
                str_as_formula_status = elem.text
        except NoSuchElementException:
            str_as_formula_status = 'empty'

        end = datetime.datetime.now()
        print(end - start)

        # UPDATE SCHEDULE
        try:
            schedule = Select(driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div/form/table/tbody/tr[32]/td[2]/select"))
            tmp_three = []
            for ele in schedule.all_selected_options:
                tmp_three.append(ele.text)
            schedule_days = ' '.join(str(e) for e in tmp_three)
        except NoSuchElementException:
            str_as_formula_status = 'empty'

        start = datetime.datetime.now()
        print(start - end)

        # FTP CREDENTIALS
        ftp_server = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[40]/td[2]/input") \
            .get_attribute('value')
        ftp_path = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[41]/td[2]/input") \
            .get_attribute('value')
        ftp_login = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[43]/td[2]/input") \
            .get_attribute('value')
        ftp_passw = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[44]/td[2]/input") \
            .get_attribute('value')

        price_list[index].append(suppliers)
        # price_list[index].append(manufacturers)
        price_list[index].append(email_box)
        price_list[index].append(client_group)
        price_list[index].append(client_categ)
        price_list[index].append(restriction_status)
        price_list[index].append(str_as_formula_status)
        price_list[index].append(schedule_days)
        price_list[index].append(ftp_server)
        price_list[index].append(ftp_path)
        price_list[index].append(ftp_login)
        price_list[index].append(ftp_passw)

    print(price_list[1])
    df = pd.DataFrame(price_list, columns=['price_num', 'file_name', 'file_link', 'suppliers',# 'manufacturers',
                                           'email_box', 'client_group', 'client_categ', 'restriction_status',
                                           'str_as_formula_status', 'schedule_days',
                                           'ftp_server', 'ftp_path', 'ftp_login', 'ftp_passw'])
    print(df.head(5))
    df.to_excel(r'C:\Users\Dell\PycharmProjects\mnk-stable\mkn_base\api\Services\PriceListInvent\export_priceList.xlsx')

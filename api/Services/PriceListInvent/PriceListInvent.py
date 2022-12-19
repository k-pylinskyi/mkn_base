# import math
# import datetime
# import requests
# from time import sleep
#
# from selenium.common import NoSuchElementException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from Services.UpdateRate.UpdateRate import login_maxi
#
# PRICE_PAGE = "https://www.maxi.parts/admin/pricelists/"
# PRICE_LIST_SETTINGS = "https://www.maxi.parts/admin/pricelists/?subj=EditTable_Form1&fn=edit&kmp_id="
# DOWNLOAD_PREFIX = "https://www.maxi.parts"
#
#
# def vyManager():
#     driver = login_maxi()
#     pricePageParse(driver)
#
#
# def pricePageParse(driver):
#     driver.get(PRICE_PAGE)
#     price_list = []
#     num_rows_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[6]/div[3]/div/div[2]/a[5]")
#     num_rows_button.click()
#     sleep(1)
#     tables = driver.find_elements(By.CLASS_NAME, "admin_edit_table")
#     for elm in tables:
#         if elm.get_attribute("data-id") == 'task_prices':
#             table = elm
#     table_t = table.find_element(By.XPATH, "./tbody")
#
#     priceList_list = table_t.find_elements(By.XPATH, "./tr")[1:10]
#     price_num_list = []
#     for row in priceList_list:
#         print("==================================")
#         link_field = row.find_element(By.CLASS_NAME, "col_file")
#         price_num = row.find_element(By.CLASS_NAME, "col_kmp_id").text
#
#         price_num_list.append(price_num)
#         print("price num: " + str(price_num))
#         try:
#             file_name = link_field.find_element(By.XPATH, "./nobr/a").get_attribute("download")
#             print("file name: " + str(file_name))
#             print("file link: " + DOWNLOAD_PREFIX + str(link_field.find_element(By.XPATH, "./nobr/a")
#                                                         .get_attribute("href")))
#         except NoSuchElementException:
#             print("file name: none")
#             print("file link: none")
#         priceList_list.append(price_num)
#
#     for el in price_num_list:
#         print("==================================")
#         link_field = row.find_element(By.CLASS_NAME, "col_file")
#         price_num = row.find_element(By.CLASS_NAME, "col_kmp_id").text
#
#         print("price num: " + str(price_num))
#         try:
#             print("file name: " + str(file_name))
#             print("file link: " + DOWNLOAD_PREFIX + str(file_link))
#         except NoSuchElementException:
#             print("file name: none")
#             print("file link: none")
#
#
#     for index, el in enumerate(price_list):
#         print("==================================")
#         print(el[0])
#         driver.get(PRICE_LIST_SETTINGS + str(el[0]))
#         # SUPPLIERS
#         select_box_suppliers = Select(driver.find_element(By.XPATH,
#                                                           "/html/body/div[1]/div/form/table/tbody/tr[6]/td[2]/select"))
#         tmp_one = []
#         for ele in select_box_suppliers.all_selected_options:
#             print("supp: " + ele.text)
#             tmp_one.append(ele.text)
#
#         # EMAIL/NAME
#         email_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[9]/td[2]/input") \
#             .get_attribute('value')
#         print("email: " + email_box)
#
#         # CLIENT CATEGORY
#         group_categ = 'empty'
#         group_categ_box = Select(driver.find_element(By.XPATH,
#                                                      "/html/body/div[1]/div/form/table/tbody/tr[11]/td[2]/select"))
#         for elem in group_categ_box.all_selected_options:
#             print("group: " + elem.text)
#             group_categ = elem.text
#
#         # FTP CREDENTIALS
#
#         ftp_server = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[40]/td[2]/input") \
#             .get_attribute('value')
#         ftp_path = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[41]/td[2]/input") \
#             .get_attribute('value')
#         ftp_login = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[43]/td[2]/input") \
#             .get_attribute('value')
#         ftp_passw = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/table/tbody/tr[44]/td[2]/input") \
#             .get_attribute('value')
#
#         print(f'FTP cred: server: {ftp_server}, path: {ftp_path}\n         login: {ftp_login}, passw: {ftp_passw}')
#         price_list[index].append(tmp_one)
#         price_list[index].append(email_box)
#         price_list[index].append(group_categ)
#         price_list[index].append(ftp_server)
#         price_list[index].append(ftp_path)
#         price_list[index].append(ftp_login)
#         price_list[index].append(ftp_passw)
#
#



from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from Services.Logger.wrapper import timeit

LOGIN_URL = "https://www.maxi.parts/admin/login/"
DRIVER_PATH = 'C:/Users/Dell/Documents/chromedriver_win32/chromedriver.exe'
LOGIN = 'nikitak_k'
PASSWORD = '3sw3ar'
SELF_PRICELIST = "https://www.maxi.parts/admin/self-pricelists/"


@timeit
def login_maxi():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,2500")
    # options=options,
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(LOGIN_URL)

    login_field = driver.find_element(By.NAME, "Login[username]")
    pass_field = driver.find_element(By.NAME, "Login[password]")
    login_button = driver.find_element(By.CLASS_NAME, "btn_accent")

    login_field.send_keys(LOGIN)
    sleep(0.5)
    pass_field.send_keys(PASSWORD)
    sleep(0.5)
    login_button.click()
    if driver.title != 'Authorization':
        print('Successfully logged in')
    else:
        print('Incorrect login/password')
    return driver


@timeit
def check_manager(supplier_list, driver):
    driver.get(SELF_PRICELIST)

    supplier_list_webelement = []
    load_list = []
    for el in supplier_list.keys():
        try:
            select = Select(driver.find_element(By.NAME, 'provider_id'))
            select.select_by_visible_text(el)
            button = driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div[3]/div[1]/form/table/tbody/tr/td[10]/input')
            button.click()
            sleep(2)
            tables = driver.find_elements(By.CLASS_NAME, "admin_edit_table")
            for elm in tables:
                if elm.get_attribute("data-id") == 'self_pricelist':
                    table = elm
            table_t = table.find_element(By.XPATH, "./tbody")

            # for load in supplier_list[el]:

            for row in table_t.find_elements(By.XPATH, "./tr")[1:]:
                supp_name = row.find_element(By.CLASS_NAME, "col_prl_name").text

                if supp_name in supplier_list[el]:
                    supplier_list_webelement.append(row)
        except NoSuchElementException:
            supp_name_load = supplier_list[el]
            supp_name = el
            supp_maxi_file_upd, supp_maxi_db_upd, supp_active = 0, 0, 0
            load_list.append([supp_name_load, supp_name, supp_maxi_file_upd, supp_maxi_db_upd, supp_active])

    for row in supplier_list_webelement:
        supp_name = row.find_element(By.CLASS_NAME, "col_short_name").text
        supp_name_load = row.find_element(By.CLASS_NAME, "col_prl_name").text
        supp_maxi_file_upd = row.find_element(By.CLASS_NAME, "col_state").text.split(' ')[-2:]
        supp_maxi_file_upd = f'{supp_maxi_file_upd[0]} {supp_maxi_file_upd[1]}'
        supp_maxi_db_upd = row.find_element(By.CLASS_NAME, "col_prl_update_file").text
        active = row.find_element(By.CLASS_NAME, "col_rule_enabled") \
            .find_elements(By.XPATH, "//input")[-1] \
            .get_attribute('value')

        supp_active = "cannot say"
        if int(active) == 1:
            supp_active = "activated"
        elif int(active) == 0:
            supp_active = "not activated"
        # print(f'Load: {supp_name_load} , supplier: {supp_name}\n'
        #       f'Price list file updated: {supp_maxi_file_upd}\n'
        #       f'price list db updated: {supp_maxi_db_upd}\n'
        #       f'price list is: {supp_active}')
        load_list.append([supp_name_load, supp_name, supp_maxi_file_upd, supp_maxi_db_upd, supp_active])
    return load_list

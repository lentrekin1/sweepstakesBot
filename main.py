import logging
import os
import platform
import random
import string
import sys
import time
from datetime import datetime

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if not os.path.isdir('logs'):
    os.mkdir('logs')

log_file = 'logs/{:%Y_%m_%d_%H}.log'.format(datetime.now())
log_format = u'%(asctime)s | %(levelname)-8s | %(message)s'
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file, encoding='utf-8')
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
root_logger.addHandler(handler)
printer = logging.StreamHandler(sys.stdout)
printer.setLevel(logging.DEBUG)
printer.setFormatter(formatter)
root_logger.addHandler(printer)

logger = logging.getLogger(__name__)

email_opts = ['lj478654', 'xxbotmail69xx', 'robertbarr4891', 'dripgang010203']
giveaway = "http://m.gvwy.io/?raflid=ccd81afb74&scale=&template=&previous_url=&referrer="

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')

if platform.system() == 'Windows':
    chromedriver = os.getcwd() + '/windows-chromedriver.exe'
else:
    chromedriver = os.getcwd() + '/linux-chromedriver'

fake = Faker()
timeout = 5
wait = 0.5
num_done = 0
num_failed = 0

logger.info('Started program')
while True:
    start = time.time()

    name = fake.name()
    email_address = ''
    for c in random.choice(email_opts):
        email_address += c
        if random.randint(1, 3) == 2:
            email_address += '.'
    if email_address[-1] == '.':
        email_address = email_address[:-1]
    email_address += '+' + ''.join(random.choices(string.ascii_letters, k=7))

    driver = webdriver.Chrome(options=chrome_options, executable_path=chromedriver)

    try:
        driver.get(giveaway)

        WebDriverWait(driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'rcwidget')))
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'fb-login-button')))
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/ul/li/div[2]')))  # prize img
        time.sleep(wait)

        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "emlogin-alt"))).click()  # use email button
        time.sleep(wait)
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/form/fieldset/div[1]/input"))).send_keys(
            name)  # name

        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/form/fieldset/div[2]/input"))).send_keys(
            email_address + '@gmail.com')# + Keys.ENTER)  # email
        time.sleep(20)
        time.sleep(wait)

        if len(driver.find_elements_by_css_selector('.entry-option-checkmark.visible')) == 0:
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/ul/li[1]/div[2]/b[9]")))
            time.sleep(wait)
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/ul/li[1]/div[2]/b[9]"))).click()  # dana fb btn
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/div[2]/fieldset/textarea"))).send_keys(
                email_address)  # dana fb field
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/a[2]"))).click()  # dana fb enter

            time.sleep(wait)

            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/ul/li[2]/div[2]/b[9]"))).click()  # candace fb button
            time.sleep(wait)
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/div[2]/fieldset/textarea"))).send_keys(
                email_address)  # candace fb field
            time.sleep(wait)
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/a[2]"))).click()  # candace fb enter
            time.sleep(wait)
            #time.sleep(20)

        driver.quit()

        num_done += 1
        end = time.time()
        logger.info(
            f'Entered with name {name} and email {email_address}, it took {end - start} seconds ({num_done} successful entry this session, {num_failed} failures in total, {(num_failed / (num_done + num_failed)) * 100}% fail rate)')
    except:
        num_failed += 1
        logger.exception(
            f'*** Entry failed ({num_done} successful entry this session, {num_failed} failures in total, {(num_failed / (num_done + num_failed)) * 100}% fail rate) ***')

        driver.quit()

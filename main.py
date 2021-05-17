import random
import time
import traceback

from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# setx BETTER_EXCEPTIONS 1

email_opts = ['lj478654', 'xxbotmail69xx', 'robertbarr4891', 'dripgang010203']
giveaway = "https://www.itsourfabfashlife.com/2021/05/ice-cream-tour-2021new-york-city.html"

fake = Faker()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
ignored = (StaleElementReferenceException, NoSuchElementException,)
timeout = 5
num_done = 0
num_failed = 0

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

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(giveaway)
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'rcwidget_xrz5gb4a')))
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_id('rcwidget_xrz5gb4a'))

        driver.switch_to.frame('rcwidget_xrz5gb4a')  # switch to giveaway iframe
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[3]/div/ul/li/div[2]'))) # prize img
        time.sleep(0.5)
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "emlogin-alt"))).click()  # use email button

        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/form/fieldset/div[1]/input"))).send_keys(name)  # name
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/form/fieldset/div[2]/input"))).send_keys(email_address + '@gmail.com' + Keys.ENTER)  # email
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/ul/li[1]/div[2]/b[9]"))).click()  # dana fb btn
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/div[2]/fieldset/textarea"))).send_keys(email_address)  # dana fb field
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/a[2]"))).click()  # dana fb enter
        time.sleep(0.5)

        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[4]/div[3]/ul/li[2]/div[2]/b[9]"))).click()  # candace fb button
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/div[2]/fieldset/textarea"))).send_keys(email_address)  # candace fb field
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/a[2]"))).click()  # candace fb enter
        time.sleep(0.1)

        driver.quit()

        num_done += 1
        end = time.time()
        print(f'Entered with name {name} and email {email_address}, it took {end - start} seconds ({num_done} successful entry this session, {num_failed} failures in total, {num_failed / (num_done + num_failed)}% fail rate)')
    except:
        driver.quit()
        traceback.print_exc()
        num_failed += 1
        print(f'*** Entry failed ({num_done} successful entry this session, {num_failed} failures in total, {num_failed / (num_done + num_failed)}% fail rate) ***')

#!/usr/bin/env python

# realpython_signin.py

'''
Open and Sign-In to Realpython website
'''

# pypi libs
from selenium import webdriver
from selenium.webdriver.common.by import By

# own module
import pmcore as pmc

## Universal vars:
passphrase = "¡Argentina Campeón del Mundo 2022! - Tres campeonatos mundiales: \
1978(Kempes), 1986('El Diego'), 2022(Messi)."
srvc = 'realpython.com'

## Get the Login Credentials for realpython.com
pmc1 = pmc.PmTable(passphrase)
usr, pwd = pmc1.get_pwd(srvc)

## Open and max the website allowing it to remain open when scrip is closed
opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
drv = webdriver.Chrome(options=opts)
drv.get('https://www.realpython.com')
drv.maximize_window()

## Sign-In
drv.find_element(By.XPATH, value='//a[@href="/account/login/?next=%2F"]').click()
drv.find_element(By.ID, "id_login").send_keys(usr)
drv.find_element(By.ID, "id_password").send_keys(pwd)
drv.find_element(By.NAME, "jsSubmitButton").click()


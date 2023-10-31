#!/usr/bin/env python

# realpython_signin.py

'''
Open and Sign-In to Realpython website
'''

# Built-in Libs
import getpass as gp
import sys

# pypi Libs
from selenium import webdriver
from selenium.webdriver.common.by import By

# own module
import pmcore as pmc

## Universal vars:
src = 'realpython jp'

## Functions:
def input_scrt(txt):
    while True:
        scrt1 = gp.getpass(f'Input {txt}: ')
        scrt2 = gp.getpass(f'Re-enter {txt}: ')
        if scrt1 == scrt2:
            break
        else:
            print(f'[ERROR] - {txt}s do not match!, try again...')
    return scrt1

### main
## Get the Login Credentials and data from PmTable
try:
    passphrase = sys.argv[1]    # pass passphrase by command line
except IndexError:
    passphrase = input_scrt('Passphrase')
except Exception as e:
    sys.exit(f'CRITICAL ERROR: {e}')

pmt = pmc.PmTable(passphrase)
usr = pmt.get_usr(src)
pwd = pmt.get_pwd(src)[0]
url = pmt.get_url(src)

## Open and max the website allowing it to remain open when scrip is closed
opts = webdriver.ChromeOptions()                # Use chrome
opts.add_experimental_option("detach", True)
drv = webdriver.Chrome(options=opts)
drv.get(url)
drv.maximize_window()

## Sign-In
drv.find_element(By.XPATH, value='//a[@href="/account/login/?next=%2F"]').click()
drv.find_element(By.ID, "id_login").send_keys(usr)
drv.find_element(By.ID, "id_password").send_keys(pwd)
drv.find_element(By.NAME, "jsSubmitButton").click()


#!/usr/bin/env python

# website_login_jm.py

'''
Open and Sign-In to Websites loaded in crypted PmTable
'''

# Built-in Libs
import getpass as gp
import sys
import time
from threading import Thread

# pypi Libs
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui            # To write proxy credentials

# own module
import pmcore as pmc


## Universal vars:
prxy = 'proxy srv'          # If you are behind a proxy
path = ""                   # If you storage your data files in a diff. dir
cipe = path + "cipe.csd"
kipe = path + 'nert'        # Actually you can storage the key in a diff. dir than the table

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

def enter_proxy_auth(proxy_username, proxy_password):
    time.sleep(1)
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')

def open_a_page(drv, url):
    drv.get(url)


### main
## Get the Service (website) and passphrase.
try:
    src = sys.argv[1]           # Service passed as first cmd line arg.
except IndexError:
    src = input('Input Service to Connect: ')

try:
    passphrase = sys.argv[2]    # pass passphrase by command line
except IndexError:
    passphrase = input_scrt('Passphrase')


## Get cnx credentials from PmTable. Service and Proxy credentials.
try:
    pmt = pmc.PmTable(passphrase, cipe, kipe)
    usr = pmt.get_usr(src)
    pwd = pmt.get_pwd(src)[0]
    url = pmt.get_url(src)
except pmc.ServiceNotFoundError as e:
    sys.exit(e)
except Exception as e:
    sys.exit(f'Critical Error getting Table: {e}')

# 2. Proxy Credentials (ad-hoc jm in univers vars):
p_usr = pmt.get_usr(prxy)
p_pwd = pmt.get_pwd(prxy)[0]
p_IP_port = pmt.get_url(prxy)


## Open and max the website (w/Chrome Options) allowing it to remain open when scrip is closed
opts = webdriver.ChromeOptions()                    # Use chrome
opts.add_experimental_option("detach", True)
drv = webdriver.Chrome(options=opts)
Thread(target=open_a_page, args=(drv, url)).start()
Thread(target=enter_proxy_auth, args=(p_usr, p_pwd)).start()
drv.implicitly_wait(7)
drv.maximize_window()


## Sign-in upon service
if src == '!donotexist':
    # Only for the unique 'if'
    pass

elif src == 'gmail jp':
    pass

elif src == 'yahoo':
    pass

elif src == 'realpython jp':
    drv.find_element(By.XPATH, value='//a[@href="/account/login/?next=%2F"]').click()
    drv.find_element(By.ID, "id_login").send_keys(usr)
    drv.find_element(By.ID, "id_password").send_keys(pwd)
    drv.find_element(By.NAME, "jsSubmitButton").click()

elif src == 'reddit':
    drv.find_element(By.XPATH, value='//span[text()="Log In"]').click()
    drv.find_element(By.ID, "login-username").send_keys(usr)
    drv.find_element(By.ID, "login-password").send_keys(pwd)










# pypi Libs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# own module
import pmcore as pmc
## Universal vars:
src = 'reddit'
passphrase = "1978, 1986, and 2022 FIFA Champ!"

pmt = pmc.PmTable(passphrase)
usr = pmt.get_usr(src)
pwd = pmt.get_pwd(src)[0]
url = pmt.get_url(src)

## Open and max the website allowing it to remain open when scrip is closed
opts = webdriver.ChromeOptions()                # Use chrome
opts.add_experimental_option("detach", True)
drv = webdriver.Chrome(options=opts)
drv.implicitly_wait(9)
drv.get(url)
drv.maximize_window()

drv.find_element(By.XPATH, value='//span[text()="Log In"]').click()
drv.find_element(By.ID, "login-username").send_keys(usr)
drv.find_element(By.ID, "login-password").send_keys(pwd)
#drv.find_element(By.XPATH, value='//span[@class="flex items-center justify-center"]').click()
#drv.find_element(By.XPATH, value='//span[text()="Log In"]').click()
# button = drv.find_element(By.XPATH, value='//span[text()="Log In"]')
# drv.execute_script("arguments[0].click();", button)
# WebDriverWait(drv, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='button' and @id='PersonalDetailsButton'][@data-controltovalidate='PersonalDetails']"))).click()
WebDriverWait(drv, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Log In"]'))).click()


quit()



import subprocess
import os

#subprocess.run(['help', 'dir'])
# subprocess.run(["python.exe",
#                 r"C:\Users\jm\git_repos\Password-Manager_w-Pandas\reddit_login.py",
#                 "1978, 1986, and 2022 FIFA Champ!"])
# subprocess.run(["python.exe",
#                 r"C:\Users\jm\git_repos\Password-Manager_w-Pandas\realpython_signin.py",
#                 "1978, 1986, and 2022 FIFA Champ!"])

exe_str = '''python.exe C:\\Users\\jm\\git_repos\\Password-Manager_w-Pandas\\realpython_signin.py "1978, 1986, and 2022 FIFA Champ!" '''
os.system(exe_str)

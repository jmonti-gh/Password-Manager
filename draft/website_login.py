# pypi libs
from selenium import webdriver
#print(webdriver.__version__)    # 4.12

opts = webdriver.ChromeOptions()
opts.add_experimental_option("detach", True)
drv = webdriver.Chrome(options=opts)
drv.get('https://google.com')
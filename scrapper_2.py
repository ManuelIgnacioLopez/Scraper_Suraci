from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import numpy as np
import time
import os
import gspread
from pyvirtualdisplay import Display
import chromedriver_autoinstaller as chromedriver
#import undetected_chromedriver as uc


display = Display(visible=0, size=(800, 800))  
display.start()

#Inicio
chromedriver.install()
driver = webdriver.Chrome()
#driver = webdriver.Chrome('./chromedriver')
#driver = uc.Chrome(use_subprocess=True)

urls_inmoclick=[
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=',
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=2',
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=3',
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=4',
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=5',
    'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&localidades=1%2C2%2C8%2C19%2C7%2C6%2C10&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=6'
    
]

driver.get(urls_inmoclick[0])
time.sleep(5)
largoUrl=driver.find_element(By.XPATH,'/html/body/nav/form/div[2]/div[2]/div/div/div[1]/h2').text
largoUrl=largoUrl.split()
largoUrl=int(largoUrl[0])
largoUrl=int(largoUrl/48)


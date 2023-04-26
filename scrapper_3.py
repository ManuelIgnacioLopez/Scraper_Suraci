from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np
import time
import os
import gspread
from pyvirtualdisplay import Display
import undetected_chromedriver as uc


display = Display(visible=0, size=(800, 800))  
display.start()

#Inicio

driver = uc.Chrome(use_subprocess=True)

urls_zp=[
    'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza.html',
    'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza-pagina-2.html',
    'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza-pagina-3.html',
  'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza-pagina-4.html',
  'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza-pagina-5.html',
  'https://www.zonaprop.com.ar/locales-comerciales-alquiler-mendoza-pagina-6.html'
]

driver.get(urls_zp[0])
time.sleep(5)


ubicacion_zp = []
metros2_zp = []  
precio_zp = []
url_zp = []
url_zp_2 = []

for mainUrl in urls_zp:
    try:
        driver.get(mainUrl)
        posts=driver.find_elements(By.XPATH, "//div[@data-posting-type='PROPERTY']")
        for post in posts:
            url='https://www.zonaprop.com.ar' + post.get_attribute("data-to-posting")
            url_zp.append(url)
    except:
        break  
url_zp=pd.Series(url_zp).drop_duplicates().tolist()
len(url_zp)

for url in url_zp:
        
        driver.get(url)
        elementFound = False
        precioElement = None
        ubicacionElement = None
        mtsElement = None
        it=0
        while(not elementFound or it==20):
                try:
                        precioElement = driver.find_element(By.CLASS_NAME,"price-items")
                        ubicacionElement = driver.find_element(By.CLASS_NAME,"title-location")
                        mtsElement = driver.find_element(By.CLASS_NAME,"section-icon-features")
                        elementFound = True
                        it +=1
                except:
                        pass
                        precio_zp.append(Null)
                        ubicacion_zp.append(Null)
                        metros2_zp.append(Null)
                    #agregar Null a los que pasa
                        
        precio_zp.append(precioElement.text)
        ubicacion_zp.append(ubicacionElement.text)
        metros2_zp.append(mtsElement.text)
        



dolarz=False    
while dolarz==False:
  try:
    driver.get('https://www.cronista.com/MercadosOnline/moneda.html?id=ARSMEP')
    ele = driver.find_element(By.XPATH,'//*[@id="market-scrll-1"]/tbody/tr/td[2]/a/div/div[2]')
    dollar=ele.text
    dollar= dollar.replace('$', '')
    dollar= dollar.replace(',', '.')
    dollar= float(dollar)
    dolarz=True
  except:
    dolarz=False
pesos=[]
for i in precio_zp:
    if i=='Consultar Precio':
        aa=i.replace('Consultar Precio', '')
        pesos.append(aa)
    
    elif i.find('USD'):
        aa=i.replace('$ ', '')
        aa=aa.replace('.', '')
        nuevo=float(aa)
        pesos.append(nuevo)
        
    elif i.find('$'):
        aa=i.replace('USD ', '')
        aa=aa.replace('.', '')
        nuevo=float(aa)*dollar
        pesos.append(nuevo)

s=[]
u_bi=[]

for i in range(0,len(ubicacion_zp)):
    u_bi.append(ubicacion_zp[i].split('\n'))

s=pd.DataFrame(u_bi, columns=['direccion','dpto', 'c'])

direccion=s.direccion
departamento=s.dpto

m_2_1=[]
m_2_2=[]

for i in range(0,len(metros2_zp)):
    m_2_1.append(metros2_zp[i].split(' '))

m_2_1=pd.DataFrame(m_2_1)

totales=m_2_1[0]
intermedio=m_2_1[2]

for i in range(0,len(metros2_zp)):
    m_2_2.append(intermedio[i].split('\n'))
    
m_2_2=pd.DataFrame(m_2_2)

cubiertos=m_2_2[1]

m2tot=totales
m2cub=cubiertos

df4= pd.DataFrame({'Precio' : precio_zp,
                                'Direccion' : direccion,
                                'Departamento de Mendoza' : departamento, 'm2 totales' : m2tot, 'm2 cubiertos' : m2cub, 'Link' : url_zp}, 
                                columns=['Precio','Direccion', 'Departamento de Mendoza', 'm2 totales','m2 cubiertos','Link'])   
    

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
    
credentials ={
  "type": "service_account",
  "project_id": "scrapper-suraci",
  "private_key_id": "4ad7fd5b6655d423e5138ab595b63611de0bad60",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDM2IseQv7ac5ju\nAt4LTkmblTSs+WNnUor+1UX3OC50JvhyV3vQEtYphVVxzWXPzGEcO8hGJXqHRLZY\n68mAdJ2JD4o+p5FU+r6as5S3SOPCNwaR/pbxkVjSaXs6HKkzK2Hwb7lFr+8/xqK6\nj5r/MjaHSf/Xpe4kl9lThZF+KKK+6edtW+6MIgUa1kyywAgzyD7jGB7YsHHYk0Ye\ngFVqfwnfvD/WZ2IaNm1vs1JznW6WnDP6L0GQh0QJ2YSDByf8I3MOqhImaISox6sz\n6eu7u2D2ztJkyfv5vYLQ66BIQbQSnllt/17lFpwQGk5cFBXHeBLXzGTxuJiIEBDU\nA1S2/wTHAgMBAAECggEADMN7W53aCluEjmQAWNz+aiLQXuzFHFWA0qMQUnieMF+T\nQHCiBtN9o6WqrsYZD2sRK/SvpGtGaLJH2F+MtSPPAxDEUOYZAJ4FDVeeLxNsGZhb\nIPKnjhK74ZRv+K17f3Q3DIexmB1/v04NqqkzA66pxiE+vz2YCpCpmnIqoB1BErsc\nmOw5v/bOtZ/I0NYJjDhHVXhWaX+zDQ43PjXU6nFAraw0sgVfJM2HH06NICtWwaSJ\nizZEtMF95hi2zRPtL6zAqHrtrEaGCWAcQ1FHGTt+c/asGa6XVC0OuEt+7jcEybkh\nmi+t+/Sbwyn7Ae3cf2As8QaEnRBPBeEiK9yAtZ6/rQKBgQD//XpGb60FIlLAemg4\n3JbH3ELAjE5MMWqmj3XsT+Zw2NJxN+ut2Mz5S8L5m+nW5my31iekYQpoz9v+RPOh\nKqZp+rgLFhkRaheaYdwN0KM5EC/x2KLbtrZKxm6vuByGUxKc9cuFnVZw1Oae523N\ne+znkd4z+oEig2tcx+lPB9JkmwKBgQDM2o/VbNLeh3tWxKfHrRdZw/5oPsW6p3yc\nZcD1tA3KpuChj6cLesODsr0h6UHgCQAsMZU1Hcveex6ZuJ+gC5NlODT46f5e6GpQ\nHKd/SQAKGAN2G1PrFTU9qT2DZ347Rj5CvARRa3KTIAKOVDcKj4WBxksfWCRtwy8P\nU38Dc3alRQKBgC0KYVhBT/UGS/8Xynyuu0zhAVG1nhUj4Lr7pOj2Sfpy+9v11d7Z\ntX7riJu4hhVMp7ZU1NbESDuWzwNXCHLD+VHOTlGNCs4Yl5yPOVOo8P8aTQVFc6oq\n5LoVXeZHA6XSugSp7qxMuafSnd05pQUxl8ZK0QjeO5hh/SLu/artGmSfAoGAGGZY\nB3XE0BiXCki2K0RkqZ58qPIBHzBf2UkNaLafhenGi7fOj8F5lDAv8uATppmr2Ze2\nS/NWmxNTG8Av0yJN1hqRxKwqTiekshIXqUOKq6kckG7E2hVWmBeWahZjpK/DLrOy\nV/hSV0/Svh0tySY7Iq/5tqwK+r/q1Qp+8GxKT3kCgYEAhR3vLPSAzHR4Fe84pFuH\n1g3XAUdLBf/YbSGMsdSuRYSwiWUIiw4DwPORk33VGqQVpB+jxs2R/SK06AMPDhIz\ncU11faR87Cbl8O6004/09YqyXK2bhtDcH7+XoNP3u2xydmg4b5jT3hBOgEbKLvVL\nWTZb/9ccjoc/hmCzj1td6XU=\n-----END PRIVATE KEY-----\n",
  "client_email": "suraci-scrapper@scrapper-suraci.iam.gserviceaccount.com",
  "client_id": "118170389175977759303",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/suraci-scrapper%40scrapper-suraci.iam.gserviceaccount.com"
}




gc = gspread.service_account_from_dict(credentials)
sh = gc.open("bbdd scrapper Suraci")

sh = gc.open("bbdd scrapper Suraci")
worksheet4= sh.get_worksheet(3)
worksheet4.update([df4.columns.values.tolist()] + df4.values.tolist(),value_input_option="USER_ENTERED")

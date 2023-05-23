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
#from pyvirtualdisplay import Display
#import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


#display = Display(visible=0, size=(800, 800))  
#display.start()

#Inicio

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#driver.implicitly_wait(30)
#driver = webdriver.Chrome('/Users/manuellopez/Desktop/chromedriver')

urls=['https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Alimentos-y-Bebidas/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Animales-y-Agro/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Autom%C3%B3viles-y-Rodados/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Deportes-y-Ocio/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Educaci%C3%B3n-y-Comunicaci%C3%B3n/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Hogar-y-Exteriores/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Indumentaria-y-Moda/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Industria-y-Manufactura/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Salud/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Servicios/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Tecnolog%C3%ADa-y-Media/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Turismo-y-Hoteler%C3%ADa/Todos/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Restaurantes/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Rotiser%C3%ADas/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Pizzerias/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Parrillas/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Comidas-R%C3%A1pidas/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Bar/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Cervecer%C3%ADa/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Pub/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Caf%C3%A9/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Helader%C3%ADa/Todos/Todos/Todos/0,100000+?order_by_field=',
      'https://negozona.com/anuncios/Busqueda/Todos/State-11-Mendoza/Gastronom%C3%ADa/Panaderias/Todos/Todos/Todos/0,100000+?order_by_field='
      
     ]
       
categoria=['Alimentos y Bebidas', 'Animales y Agro', 'Automóviles y Rodados', 'Deportes y Ocio', 'Educación y Comunicación',  'Hogar y Exteriores', 'Indumentaria y Moda', 'Industria y Manufactura', 'Salud', 'Servicios', 'Tecnología y Media', 'Turismo y Hotelería', 'Gastronomía - Restaurantes', 'Gastronomía - Rotiserias','Gastronomía - Pizzerias', 'Gastronomía - Parrillas', 'Gastronomía - Comidas Rapidas', 'Gastronomía - Bar', 'Gastronomía - Cerveceria', 'Gastronomía - Pub', 'Gastronomía - Cafe',  'Gastronomía - Heladeria', 'Gastronomía - Panaderias']

Nombres_marca = []
Inv_totalmin_marca = []
cate = []
count=0
for aa in range(0, len(urls)):
    driver.get(urls[aa])
    marca = driver.find_elements(By.CLASS_NAME,'title_publication')
    
    inv_tot_min = driver.find_elements(By.CLASS_NAME,'price_publication')

    for ele in marca:
        Nombres_marca.append(ele.text)
        count+=1
    for ele in inv_tot_min:
        Inv_totalmin_marca.append(ele.text)

    for item in range(0, count):
        cate.append(categoria[aa])
    count=0    
Nombres_marca = Nombres_marca[::2]
cate = cate[::2]
dolarz=False    
while dolarz==False:
  try:
    driver.get('https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB')
    ele = driver.find_element(By.XPATH,'//*[@id="market-scrll-1"]/tbody/tr/td[2]/a/div/div[2]')
    dollar=ele.text
    dollar= dollar.replace('$', '')
    dollar= dollar.replace(',', '.')
    dollar= float(dollar)
    dolarz=True
  except:
    dolarz=False

dolar=[]
for i in Inv_totalmin_marca:
    if i=='Consultar Precio':
        aa=i.replace('Consultar Precio', '')
        dolar.append(aa)
    
    elif i.find('USD'):
        aa=i.replace('$ ', '')
        aa=aa.replace('.', '')
        nuevo=float(aa)/dollar
        dolar.append(nuevo)
        
    elif i.find('$'):
        aa=i.replace('USD ', '')
        aa=aa.replace('.', '')
        dolar.append(float(aa))
len(dolar)     


Data= pd.DataFrame({'CATEGORIA' : cate,
                                'MARCA' : Nombres_marca,
                                'INVERSION MINIMA INICIAL' : Inv_totalmin_marca, 'INVERSION_MINIMA_INICIAL_EN_DOLARES' : dolar, 'valor dolar' : dollar}, 
                                columns=['CATEGORIA','MARCA', 'INVERSION MINIMA INICIAL', 'INVERSION_MINIMA_INICIAL_EN_DOLARES','valor dolar'])


df = pd.DataFrame(Data)

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


worksheet2= sh.get_worksheet(1)
worksheet2.clear()
worksheet2.update([df.columns.values.tolist()] + df.values.tolist(),value_input_option="USER_ENTERED")

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

urls_inmoclick=['https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&ordenar=menor-precio&q=mendoza&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=',
      'https://www.inmoclick.com.ar/locales-comerciales-en-alquiler?favoritos=0&limit=48&prevEstadoMap=&ordenar=menor-precio&q=mendoza&lastZoom=13&precio%5Bmin%5D=&precio%5Bmax%5D=&moneda=1&sup_cubierta%5Bmin%5D=&sup_cubierta%5Bmax%5D=&expensas%5Bmin%5D=&expensas%5Bmax%5D=&page=2'
     ]



ubicacion = []
metros2 = []
precio = []
url = []

path_ubi=[]
path_m2=[]
path_p=[]
path_ur=[]
for aa in range(1, 49):
    path_ubi.append('//*[@id="articles-and-map"]/div[1]/section/div/section/div/div/div[' + str(aa) + ']/article/div[2]/p')
for aa in range(1, 49):
    path_m2.append('//*[@id="articles-and-map"]/div[1]/section/div/section/div/div/div[' + str(aa) + ']/article/div[3]/div/div[2]/span')
for aa in range(1, 49):
    path_p.append('//*[@id="articles-and-map"]/div[1]/section/div/section/div/div/div[' + str(aa) + ']/article')
for aa in range(1, 49):
    path_ur.append('/html/body/div[3]/div[1]/section/div/section/div/div/div[' + str(aa) + ']/article/div[2]/h4/a') 

 for aa in range(0, len(urls_inmoclick)):
    driver.get(urls_inmoclick[aa])
    for ab in range(0, 48):
        pr = driver.find_element(By.XPATH,path_p[ab]).text
        precio.append(pr)
    for ad in range(0, 48):
        try:
            ubi = driver.find_element(By.XPATH,path_ubi[ad]).text
            m2 = driver.find_element(By.XPATH,path_m2[ad]).text
        except NoSuchElementException as e :
            ur = None 
        ubicacion.append(ubi)
        metros2.append(m2)
    for ab in range(0, 48):
        driver.switch_to.window(driver.window_handles[0])
        try:
            ur = driver.find_element(By.XPATH,path_ur[ab]).click()
        except NoSuchElementException as e :
            ur = None 
        driver.switch_to.window(driver.window_handles[-1])
        url.append(driver.current_url)
        
precioo = []
precio1 =[]

for ac in range(0, 48):
    precio1.append(precio[ac].split('$'))
s=pd.DataFrame(precio1, columns=['a','b', 'c'])

for ac in range(0, 48):
    precioo.append(s.b[ac].split('\n'))
   
d=pd.DataFrame(precioo)

d.columns = ['Precio', 'Lugar','2', 'mtot', 'mcubiertos', '5','6']

d['Url']=url
d['Metros2']=metros2
d['Direccion']=ubicacion

df2 = pd.DataFrame(d)

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
worksheet3= sh.get_worksheet(2)
worksheet3.update([df2.columns.values.tolist()] + df2.values.tolist(),value_input_option="USER_ENTERED")



"""
Elaborado por: Diego Rojas
Fecha: 20 Junio 2020
"""
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
from pymongo import MongoClient

#Creamos una colección en Mongodb donde vamos a guardar los datos de los libros
client = MongoClient('localhost')
db = client['amazon']
col = db['data_science_books2']

# Definimos el User Agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome(executable_path=r"C:\Users\dar12\Downloads\Web Scraping\chromedriver.exe", chrome_options=opts)

#Establecemos la pagina semilla
driver.get('https://www.amazon.com/s?k=data+science&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss')

#Numero de paginas que voy a realizar el proceso de scraping
pagina_maxima = 15
pagina_actual = 1

#Antes de continuar, creamos una función que elimine la tabulación y saltos de linea
def limpieza(texto):
      texto_corregido=texto.replace('\n', '').replace('\t', '')
      return texto_corregido

# Ejecutar el proceso hasta que llegue a la pagina maxima
while pagina_maxima >= pagina_actual:

  WebDriverWait(driver, 20).until(
  EC.presence_of_all_elements_located((By.XPATH, '//div[@class="sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"]//div//a[@class="a-link-normal a-text-normal"]')))

  links_productos = driver.find_elements(By.XPATH, '//div[@class="sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"]//div//a[@class="a-link-normal a-text-normal"]')
  links_de_la_pagina = []
  for a_link in links_productos:
    links_de_la_pagina.append(a_link.get_attribute("href"))

  for link in links_de_la_pagina:

    try:
      # Extraigo los links de cada uno de los libros de la pagina
      driver.get(link)

      try:
            autor = driver.find_element(By.XPATH, '//span[@class="author notFaded"]').text
            autor=autor.split(' (')[0]
      except:
            autor='N.D' 
      try:
            titulo = driver.find_element(By.XPATH, '//div[@class="a-container"]//div//div[@class="a-section a-spacing-none"]//h1//span[1]').text
            titulo=titulo.replace('\n', '').replace('\t', '')
      except:
            titulo='N.D' 
      try:
            reviews = driver.find_element(By.XPATH, '//span[@class="a-size-base a-nowrap"]').text
            reviews=reviews.split(' out')[0]
            reviews=float(reviews)
      except:
            reviews=float(0)
      try:
            ratings = driver.find_element(By.XPATH, '//*[@id="acrCustomerReviewText"]').text
            ratings=ratings.split(' ratings')[0].replace(' rating','')
            ratings=int(ratings)
      except:
            reviews=int(0)
      try:
            precio_nuevo = driver.find_element(By.XPATH, '//*[@id="newBuyBoxPrice"]').text
            precio_nuevo=precio_nuevo.replace('$', '')
            precio_nuevo=float(precio_nuevo)
      except:
            precio_nuevo=float(0)
      try:
            precio_alquiler = driver.find_element(By.XPATH, '//*[@id="rentPrice"]').text
            precio_alquiler=precio_alquiler.replace('$', '')
            precio_alquiler=float(precio_alquiler)
      except:
            precio_alquiler=float(0)
      try:
            precio_etq1 = driver.find_element(By.XPATH, '//span[@class="a-button-inner"]//a//span[@class="a-size-base a-color-secondary"]').text
            precio_etq1=precio_etq1.replace('$', '')
            precio_etq1=float(precio_etq1)
      except:
            precio_etq1=float(0)
      try:
            precio_etq2 = driver.find_element(By.XPATH, '//span[@class="a-button-inner"]//a//span[@class="a-color-base"]').text
            precio_etq2=precio_etq2.replace('$', '')
            precio_etq2=float(precio_etq2)
      except:
            precio_etq2=float(0)
      try:
            item_1 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[1]').text
            item_1=limpieza(item_1)
      except:
            item_1='N.D'
      try:
            item_2 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[2]').text
            item_2=limpieza(item_2)
      except:
            item_2='N.D'      
      try:
            item_3 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[3]').text
            item_3=limpieza(item_3)
      except:
            item_3='N.D'      
      try:
            item_4 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[4]').text
            item_4=limpieza(item_4)
      except:
            item_4='N.D'      
      try:
            item_5 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[5]').text
            item_5=limpieza(item_5)
      except:
            item_5='N.D'
      try:
            item_6 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[6]').text
            item_6=limpieza(item_6)
      except:
            item_6='N.D'
      try:
            item_7 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[7]').text
            item_7=limpieza(item_7)
            item_7=item_7.replace(' (View shipping rates and policies)', '')
      except:
            item_7='N.D'
      try:
            item_8 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[8]').text
            item_8=limpieza(item_8)
      except:
            item_8='N.D'
      try:
            item_9 = driver.find_element(By.XPATH, '//*[@id="productDetailsTable"]/tbody/tr/td/div/ul/li[9]').text
            item_9=limpieza(item_9)
      except:
            item_9='N.D'
      #Agregamos una variable con la fecha en que estamos haciendo la extracción
      fecha_subida=str(date.today())
      
      #Inserto los datos en la colección en Mongodb
      col.insert_one({
        'autor': autor,
        'titulo': titulo,
        'reviews':reviews,
        'ratings':ratings,
        'precio_nuevo':precio_nuevo,
        'precio_alquiler':precio_alquiler,
        'precio_otro_1':precio_etq1,
        'precio_otro_2':precio_etq2,
        'item_1':item_1,
        'item_2':item_2,
        'item_3':item_3,
        'item_4':item_4,
        'item_5':item_5,
        'item_6':item_6,
        'item_7':item_7,
        'item_8':item_8,
        'item_9':item_9,
        'fecha_subida':fecha_subida
      })

      # Piso el boton de retroceso
      driver.back()
    except Exception as e:
      print (e)
      # Si sucede algún error regreso y sigo con el siguiente libro.
      driver.back()

  # Logica de deteccion de fin de paginacion
  try:
    # Le doy click al boton siguiente; sino existe se termina el proceso
    puedo_seguir_horizontal = driver.find_element_by_class_name('a-last')
    puedo_seguir_horizontal.click()

  except: 
    break

  pagina_actual += 1

driver.close()
 
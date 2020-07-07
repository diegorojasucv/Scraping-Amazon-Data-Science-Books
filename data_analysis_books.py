"""
OBJETIVO: Encontrar el top 10 de libros de Data Scientist con mayor rating y cantidad de reviews.
ELABORADO POR: Diego Rojas
FECHA DE ELABORACIÓN: Julio 2020
"""

import pandas as pd
import numpy as np
import re
from pymongo import MongoClient
from matplotlib import pyplot as plt
import seaborn as sns

# Seleccionamos la base de datos y la coleccion en Mongodb
client = MongoClient('localhost')
db = client['amazon']
col = db['data_science_books']

df = pd.DataFrame.from_dict(col.find(
                                    {},
                                    {
                                        '_id':0, 
                                        'autor':1, 
                                        'titulo':1, 
                                        'reviews':1, 
                                        'ratings':1, 
                                        'precio_nuevo':1, 
                                        'precio_alquiler':1, 
                                        'precio_otro_1':1, 
                                        'precio_otro_2':1
                                    }))

# Creamos una nueva variable con el precio maximo
df['precio_maximo'] = df[['precio_nuevo','precio_alquiler','precio_otro_1','precio_otro_2']].max(axis=1)
df = df.drop(columns=['precio_nuevo','precio_alquiler','precio_otro_1','precio_otro_2'])

# Eliminamos libros duplicados
df = df.drop_duplicates()

'''
Ahora realizamos los siguientes filtros:
    1) reviews mayor a cero
    2) rating mayor a 80
    3) titulos que hagan referencia a Data Science, Machine Learning o Statistical
''' 
# Primero vamos a corregir los valores que poseen comas (,)
ratings_modified=[]
for i in df.ratings:
    x = int(re.sub('\,', '', str(i)))
    #print(x)
    ratings_modified.append(x)

# Remplazamos por el valor anterior
df['ratings'] = pd.Series(ratings_modified, index=df.index)

# Filtramos por los tipos de libros mencionados anteriormente
filter_list = [ 'chine' # Machine Learning
                ,'cien' # Data Science
                ,'tatis' # Statistical
                ]

df_filtered = df[(df.reviews>0) & 
                 (df.ratings>80) & 
                 (df.titulo.str.contains('|'.join(filter_list)))]

df_filtered = df_filtered.sort_values(by = ['reviews', 'ratings'] , ascending = False)

# Excluimos algunos autores que no se relacionan con el tema
no_author = ['Mert Damlapinar', 'Charles Wheelan', 'Brian Christian', 
             'Foster Provost', 'John W. Foreman', 'Jake VanderPlas', 
             'Austin Ruse', 'Wladston Ferreira Filho']

# Seleccionamos el top de 10 de libros con mayor reviews y numero de calificaciones
df_filtered = df_filtered[~df_filtered.autor.str.contains('|'.join(no_author))].head(10)

# Graficomos el top 10 de libros

sns.barplot(x='reviews', y='titulo', data=df_filtered
            , palette="Blues_d")


"""
OBJETIVO: 
    - Calcular el porcentaje de apariciones de los lenguages de programacion y bibliotecas en las solicitudes de empleo para la posición de Data Scientist.
CREADO POR: Diego Rojas
ULTIMA VEZ EDITADO: Julio 2020
"""

import pandas as pd
import numpy as np
from pymongo import MongoClient
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec

# Seleccionamos la base de datos y la coleccion en Mongodb
client = MongoClient('localhost')
db = client['indeed']
col = db['data_scientist_jobs']

df = pd.DataFrame.from_dict(col.find({},{'_id':0, 'title':1, 'item1':1, 'item2':1, 'item3':1}))


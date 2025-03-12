import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.decomposition import NMF
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score


data = pd.read_csv("./dataset/recipes.csv")

data_procesada = data.drop(columns=["AggregatedRating", "ReviewCount", "RecipeYield", "CookTime"])
data_procesada.dropna(inplace=True)

columns = [
    'Calories',
    'FatContent',
    'SaturatedFatContent',
    'CholesterolContent',
    'SodiumContent',
    'CarbohydrateContent',
    'FiberContent',
    'SugarContent',
    'ProteinContent'
]

def eliminar_sobrante(row): # elimina la c y los parentesis que roodean el texto en algunas columnas y las ocmillas sobrantes
    columnas = ["Keywords", "RecipeIngredientQuantities", "RecipeIngredientParts"]
    for nombre in columnas:
        row[nombre] = row[nombre][2:-1].replace('"', '').split(', ')
            
    return row

data_procesada = data_procesada.apply(eliminar_sobrante, axis=1)


condicion = (data_procesada[columns[0]] / data_procesada["RecipeServings"] > 2000) | (data_procesada[columns[0]] == 0)
condicion2 = (data_procesada[columns[0]] >= 0)
for i in range(1, len(columns)):
    condicion |= (data_procesada[columns[i]] / data_procesada["RecipeServings"] > 1000)
    condicion2 &= (data_procesada[columns[i]] == 0)
    
data_valores_altos = data_procesada.copy()[condicion | condicion2]

data_procesada = data_procesada[~(condicion | condicion2)]

data_procesada.to_csv('./dataset/recipes_procesado.csv', index=False)

data_entrenamiento = data_procesada.drop(columns=["AuthorId", "AuthorName", "DatePublished", "PrepTime",
                   "Images", "Name", "RecipeInstructions", "Description"])

data_entrenamiento.to_csv('./dataset/recipes_entrenamiento.csv', index=False)
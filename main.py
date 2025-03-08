from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from joblib import load
from usuario import Usuario
from valores_saludables import ValoresSaludables

class RecipeRecomender():
    def __init__(self, recipes, model, nn=NearestNeighbors(n_neighbors=10, algorithm='brute'),scaler=MinMaxScaler()):
        self.recipes = recipes
        self.scaler = scaler
        self.model = model
        self.nn = nn

        self.scaler.fit(self.recipes[["Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent"]].to_numpy())
    
    def recomend(self, **kwars):
        
        nutritional_values = {
            "calorias": kwars.get("calorias", None) or self.recipes["Calories"].mean(),
            "grasas": kwars.get("grasas", None) or self.recipes["FatContent"].mean(),
            "grasas_saturadas": kwars.get("grasas_saturadas", None) or self.recipes["SaturatedFatContent"].mean(),
            "colesterol": kwars.get("colesterol", None) or self.recipes["CholesterolContent"].mean(),
            "sodio": kwars.get("sodio", None) or self.recipes["SodiumContent"].mean(),
            "carbohidratos": kwars.get("carbohidratos", None) or self.recipes["CarbohydrateContent"].mean(),
            "fibra": kwars.get("fibra", None) or self.recipes["FiberContent"].mean(),
            "azucares": kwars.get("azucares", None) or self.recipes["SugarContent"].mean(),
            "proteinas": kwars.get("proteinas", None) or self.recipes["ProteinContent"].mean(),
        }
        valores = [list(nutritional_values.values())]
        procesed_input = np.array(self.scaler.transform(valores))

        clasificacion = self.model.predict(procesed_input)[0]

        recipes = self.recipes[self.recipes["cluster"] == clasificacion]

        self.nn.fit(recipes[["Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent"]].to_numpy())
        indices = self.nn.kneighbors(procesed_input, return_distance=False)[0]
        
        recomended_recipes = self.recipes.iloc[indices]
        return recomended_recipes


def main():

    model = load("./models/model.joblib")

    recipes = pd.read_csv("./dataset/recipes_procesado.csv")
    recipes_clustering = pd.read_csv("./dataset/recipes_entrenamiento_clusterizada.csv")

    recipes["cluster"] = recipes_clustering["cluster"]

    recomender = RecipeRecomender(recipes, model=model)


    usuario = Usuario(nombre="Juan", peso=70, altura=170, edad=20, genero="hombre", nivel_ejercicio="activo")
    valores_saludables = ValoresSaludables(usuario)


    recomended_recipes = recomender.recomend(**valores_saludables.__dict__)

    print(recomended_recipes)

    recomended_recipes[ ["Calories", "FatContent", "SaturatedFatContent", "CholesterolContent", "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent"] ].to_csv("./dataset/recomendaciones.csv", index=False)

if __name__ == "__main__":
    main()
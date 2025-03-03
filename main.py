from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class RecipeRecomender():
    def __init__(self, recipes, scaler=StandardScaler(), model=NearestNeighbors(metric="euclidean", algorithm='brute')):
        self.recipes = recipes
        self.scaler = scaler
        self.model = model

        procesed_recipes = self.scaler.fit_transform(self.recipes.iloc[:,6:15].to_numpy())

        model.fit(procesed_recipes)
    
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

        indices = self.model.kneighbors(procesed_input, return_distance=False)
        recomended_recipes = self.recipes.iloc[indices]
        return recomended_recipes


def main():

    recipes = pd.read_csv("./dataset/recipes_entrenamiento.csv")

    recomender = RecipeRecomender(recipes)

    print(recomender.recomend(calorias=100))




if __name__ == "__main__":
    main()
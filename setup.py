import kagglehub
import os

# Especificar el nombre o ruta de la carpeta
nombre_carpeta = "dataset"

# Crear la carpeta si no existe
if not os.path.exists(nombre_carpeta):
    os.makedirs(nombre_carpeta)

# Download latest version
path = kagglehub.dataset_download("/irkaal/foodcom-recipes-and-reviews", destination="dataset")

print("Path to dataset files:", path)
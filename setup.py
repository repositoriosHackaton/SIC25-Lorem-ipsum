import kagglehub
import os
import shutil

# Especificar el nombre o ruta de la carpeta
nombre_carpeta = "dataset"

# Especifica el nombre del dataset en Kaggle
dataset_path = "irkaal/foodcom-recipes-and-reviews"

# Download latest version
path = kagglehub.dataset_download(dataset_path)

# Crear la carpeta si no existe
if not os.path.exists(nombre_carpeta):
    os.makedirs(nombre_carpeta)

# Mover el archivo descargado a la carpeta deseada
for filename in os.listdir(downloaded_path):
    shutil.move(os.path.join(downloaded_path, filename), nombre_carpeta)

print(f"Dataset descargado y movido a la carpeta: {nombre_carpeta}")

print("Path to dataset files:", path)

import tkinter as tk
from tkinter import ttk, messagebox
import main
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import requests
from io import BytesIO
import regresoresRece
from datetime import datetime


# Función para cargar y mostrar una imagen desde una URL
def cargar_imagen_desde_url(label_img,url):
    try:
        # Descargar la imagen desde la URL
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la descarga fue exitosa

        # Abrir la imagen con Pillow
        imagen_pillow = Image.open(BytesIO(response.content))

        # Redimensionar la imagen si es necesario (opcional)
        imagen_pillow = imagen_pillow.resize((200, 200))

        # Convertir la imagen a un formato compatible con Tkinter
        imagen_tk = ImageTk.PhotoImage(imagen_pillow)

        # Mostrar la imagen en un Label
        label_img.config(image=imagen_tk)
        label_img.image = imagen_tk  # Guardar una referencia para evitar que la imagen sea eliminada por el recolector de basura
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        label_img.config(text="[Error al cargar la imagen]")


# Función para cambiar a la página roja
def cambiar_a_pagina_roja():

    # Frame para la página roja (inicialmente oculto)
    global frame_pagina_rojas
    frame_pagina_roja = tk.Frame(ventana, bg="#ffcccc")
    
    # Ocultar el frame del formulario
    frame_formulario.pack_forget()

    # Mostrar el frame de la página roja
    frame_pagina_roja.pack(fill="both", expand=True)

    # Limpiar el contenido anterior del frame de la página roja
    for widget in frame_pagina_roja.winfo_children():
        widget.destroy()

    recomendaciones = pd.read_csv("./dataset/recomendaciones.csv")
    #df = pd.read_csv("./dataset/recipes.csv")

    recomendaciones_df = recomendaciones.to_dict('index')

    list_datos_comida = [valor for valor in recomendaciones_df.values()]

    # Función para formatear el tiempo
    def format_time(time_str):
        if "H" in time_str:
            hours = time_str.split("H")[0].replace("PT", "")
            minutes = time_str.split("H")[1].replace("M", "")
            return f"{hours}h {minutes}m"
        else:
            minutes = time_str.replace("PT", "").replace("M", "")
            return f"{minutes}m"

    # Función para mostrar más información
    def show_more_info(receta):
        info_window = tk.Toplevel()
        info_window.title(receta["Name"])
        info_window.geometry("400x300")

        # Instrucciones
        tk.Label(info_window, text="Instrucciones:", font=("Arial", 12, "bold")).pack(pady=5)
        listo = main.corregir_instruccion(receta["RecipeInstructions"])
        for step in listo:
            tk.Label(info_window, text=f"- {step}", wraplength=380, justify="left").pack(anchor="w")

        # Nutrientes
        tk.Label(info_window, text="Nutrientes:", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Label(info_window, text=f"Calories: {receta['Calories']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"FatContent: {receta['FatContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"SaturatedFatContent: {receta['SaturatedFatContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"CholesterolContent: {receta['CholesterolContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"SodiumContent: {receta['SodiumContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"CarbohydrateContent: {receta['CarbohydrateContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"FiberContent: {receta['FiberContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"SugarContent: {receta['SugarContent']}", wraplength=380, justify="left").pack(anchor="w")
        tk.Label(info_window, text=f"ProteinContent: {receta['ProteinContent']}", wraplength=380, justify="left").pack(anchor="w")

         # Estilo
        estilo = ttk.Style()
        estilo.configure("Treeview", font=("Arial", 12), rowheight=25)
        estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        
        # Crear la tabla
        columnas = ("Ingrediente", "Precio Actual", "Precio Futuro")
        tabla = ttk.Treeview(root, columns=columnas, show="headings")
        
        # Configurar las columnas
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="center")

        ingredientes_lista = corregir_instruccion(receta["RecipeIngredientParts"])
        modelosLineales = regresoresRece.regresorIngredientes(ingredientes_lista)

        def isModelo(a, fecha):
            if a == None:
                return "No Info",
            else:
                return a.predict(fecha)
        
        # Insertar los datos en la tabla
        for i, (ingrediente, precio) in enumerate(zip(ingredientes_lista, )):
            tabla.insert("", "end", values=(ingrediente, f"${precio}", ""))
        
        # Posicionar la tabla en la ventana
        tabla.pack(pady=20)

    
    # Frame con scroll
    canvas = tk.Canvas(frame_pagina_roja, bg="#ffcccc")
    scrollbar = ttk.Scrollbar(frame_pagina_roja, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mostrar cada receta
    for receta in list_datos_comida:
        frame = ttk.Frame(scrollable_frame, padding="10", style="Card.TFrame")
        frame.pack(fill="x", pady=5, padx=10)

        # Nombre
        tk.Label(frame, text=receta["Name"], font=("Arial", 14, "bold")).pack(anchor="w")

        # Imagen (simulada con un label)
        label_img = ttk.Label(frame)
        label_img.pack(pady=5)

        list_img = main.corregir_links(receta["Images"])

        cargar_imagen_desde_url(label_img , list_img[0])

        # Descripción
        tk.Label(frame, text=receta["Description"], wraplength=550, justify="left").pack(anchor="w")

        # Tiempos
        tiempos = f"Preparación: {format_time(receta['PrepTime'])}, Total: {format_time(receta['TotalTime'])}"
        tk.Label(frame, text=tiempos, font=("Arial", 10, "italic")).pack(anchor="w")

        # Botón "Ver más"
        ttk.Button(frame, text="Ver más", command=lambda r=receta: show_more_info(r)).pack(pady=10)

    # Estilos
    style = ttk.Style()
    style.configure("Card.TFrame", background="white", borderwidth=2, relief="raised")


# Función para validar y procesar los datos del formulario
def procesar_formulario():
    # Obtener los valores ingresados por el usuario
    nombre = entry_nombre.get()
    peso = entry_peso.get()
    altura = entry_altura.get()
    edad = entry_edad.get()
    genero = entry_genero.get()
    nivel_ejercicio = entry_nivel_ejercicio.get()

    # Validar que todos los campos estén completos
    if not nombre or not peso or not altura or not edad or not genero or not nivel_ejercicio:
        messagebox.showwarning("Error", "Por favor, completa todos los campos.")
        return

    # Convertir peso, altura y edad a los tipos correctos
    try:
        peso = float(peso)
        altura = float(altura)
        edad = int(edad)
    except ValueError:
        messagebox.showwarning("Error", "Peso, altura y edad deben ser números válidos.")
        return


    
    # Mostrar los datos en un mensaje (esto es opcional)
    #mensaje = f"Nombre: {nombre}\nPeso: {peso} kg\nAltura: {altura} cm\nEdad: {edad} años\nGénero: {genero}\nNivel de ejercicio: {nivel_ejercicio}"
    #messagebox.showinfo("Datos ingresados", mensaje)

    main.getRecomendacionesPersona(nombre, peso, altura, edad, genero, nivel_ejercicio)

    # Cambiar a la página roja
    cambiar_a_pagina_roja()

def run():
    # Crear la ventana principal
    global ventana
    ventana = tk.Tk()
    ventana.title("Formulario de Usuario")
    ventana.geometry("600x500")
    
    # Frame para el formulario
    global frame_formulario
    frame_formulario = tk.Frame(ventana)
    frame_formulario.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Campos del formulario
    tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="w")
    global entry_nombre
    entry_nombre = tk.Entry(frame_formulario)
    entry_nombre.grid(row=0, column=1, pady=5)
    
    tk.Label(frame_formulario, text="Peso (kg):").grid(row=1, column=0, sticky="w")
    global entry_peso 
    entry_peso = tk.Entry(frame_formulario)
    entry_peso.grid(row=1, column=1, pady=5)
    
    tk.Label(frame_formulario, text="Altura (cm):").grid(row=2, column=0, sticky="w")
    global entry_altura
    entry_altura = tk.Entry(frame_formulario)
    entry_altura.grid(row=2, column=1, pady=5)
    
    tk.Label(frame_formulario, text="Edad:").grid(row=3, column=0, sticky="w")
    global entry_edad
    entry_edad = tk.Entry(frame_formulario)
    entry_edad.grid(row=3, column=1, pady=5)
    
    tk.Label(frame_formulario, text="Género:").grid(row=4, column=0, sticky="w")
    global entry_genero
    sexo = ["hombre", "mujer"]
    entry_genero = tk.StringVar(frame_formulario)

    option_menu = tk.OptionMenu(frame_formulario, entry_genero, *sexo)
    option_menu.grid(row=4, column=1, pady=5)
    #sentry_genero = tk.Entry(frame_formulario)
    
    
    tk.Label(frame_formulario, text="Nivel de ejercicio:").grid(row=5, column=0, sticky="w")
    global entry_nivel_ejercicio
    actividad = ["sedentario","ligero","moderado","activo","muy activo"]
    entry_nivel_ejercicio = tk.StringVar(frame_formulario)
    option_menu2 = tk.OptionMenu(frame_formulario, entry_nivel_ejercicio, *actividad)
    option_menu2.grid(row=5, column=1, pady=5)
    #entry_nivel_ejercicio = tk.Entry(frame_formulario)
    #entry_nivel_ejercicio.grid(row=5, column=1, pady=5)
    
    # Botón para procesar el formulario
    boton_enviar = tk.Button(frame_formulario, text="Enviar", command=procesar_formulario)
    boton_enviar.grid(row=6, column=0, columnspan=2, pady=10)
    
    

    # Ejecutar la ventana
    ventana.mainloop()



if __name__=="__main__":
    run()
import tkinter as tk
from tkinter import ttk, messagebox

# Función para cambiar a la página roja
def cambiar_a_pagina_roja():
    # Ocultar el frame del formulario
    frame_formulario.pack_forget()

    # Mostrar el frame de la página roja
    frame_pagina_roja.pack(fill="both", expand=True)

    # Limpiar el contenido anterior del frame de la página roja
    for widget in frame_pagina_roja.winfo_children():
        widget.destroy()

    # Datos de ejemplo
    list_datos_comida = [
        {
            "nombre": "Pizza Margarita",
            "descripcion": "Una deliciosa pizza con tomate, mozzarella y albahaca.",
            "imagen": "pizza.jpg",  # Cambia por la ruta de una imagen real
            "cooktime": "PT30M",
            "preptime": "PT20M",
            "totaltime": "PT50M",
            "repicetsIntrutions": [
                "Preparar la masa.",
                "Extender la salsa de tomate.",
                "Añadir mozzarella y albahaca.",
                "Hornear durante 30 minutos."
            ],
            "nutrientes": {
                "calorias": "250 kcal",
                "grasas": "10 g",
                "proteinas": "12 g"
            }
        },
        {
            "nombre": "Ensalada César",
            "descripcion": "Ensalada fresca con pollo, crutones y aderezo César.",
            "imagen": "ensalada.jpg",  # Cambia por la ruta de una imagen real
            "cooktime": "PT10M",
            "preptime": "PT15M",
            "totaltime": "PT25M",
            "repicetsIntrutions": [
                "Lavar y cortar la lechuga.",
                "Cocinar el pollo y cortarlo en tiras.",
                "Mezclar con crutones y aderezo."
            ],
            "nutrientes": {
                "calorias": "180 kcal",
                "grasas": "8 g",
                "proteinas": "15 g"
            }
        }
    ]

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
        info_window.title(receta["nombre"])
        info_window.geometry("400x300")

        # Instrucciones
        tk.Label(info_window, text="Instrucciones:", font=("Arial", 12, "bold")).pack(pady=5)
        for step in receta["repicetsIntrutions"]:
            tk.Label(info_window, text=f"- {step}", wraplength=380, justify="left").pack(anchor="w")

        # Nutrientes
        tk.Label(info_window, text="Nutrientes:", font=("Arial", 12, "bold")).pack(pady=10)
        for key, value in receta["nutrientes"].items():
            tk.Label(info_window, text=f"{key.capitalize()}: {value}", wraplength=380, justify="left").pack(anchor="w")

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
        tk.Label(frame, text=receta["nombre"], font=("Arial", 14, "bold")).pack(anchor="w")

        # Imagen (simulada con un label)
        tk.Label(frame, text="[Imagen]", bg="white", width=50, height=10).pack(pady=5)

        # Descripción
        tk.Label(frame, text=receta["descripcion"], wraplength=550, justify="left").pack(anchor="w")

        # Tiempos
        tiempos = f"Preparación: {format_time(receta['preptime'])}, Cocción: {format_time(receta['cooktime'])}, Total: {format_time(receta['totaltime'])}"
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
    mensaje = f"Nombre: {nombre}\nPeso: {peso} kg\nAltura: {altura} cm\nEdad: {edad} años\nGénero: {genero}\nNivel de ejercicio: {nivel_ejercicio}"
    messagebox.showinfo("Datos ingresados", mensaje)

    # Cambiar a la página roja
    cambiar_a_pagina_roja()


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Usuario")
ventana.geometry("600x500")

# Frame para el formulario
frame_formulario = tk.Frame(ventana)
frame_formulario.pack(fill="both", expand=True, padx=20, pady=20)

# Campos del formulario
tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="w")
entry_nombre = tk.Entry(frame_formulario)
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(frame_formulario, text="Peso (kg):").grid(row=1, column=0, sticky="w")
entry_peso = tk.Entry(frame_formulario)
entry_peso.grid(row=1, column=1, pady=5)

tk.Label(frame_formulario, text="Altura (cm):").grid(row=2, column=0, sticky="w")
entry_altura = tk.Entry(frame_formulario)
entry_altura.grid(row=2, column=1, pady=5)

tk.Label(frame_formulario, text="Edad:").grid(row=3, column=0, sticky="w")
entry_edad = tk.Entry(frame_formulario)
entry_edad.grid(row=3, column=1, pady=5)

tk.Label(frame_formulario, text="Género:").grid(row=4, column=0, sticky="w")
entry_genero = tk.Entry(frame_formulario)
entry_genero.grid(row=4, column=1, pady=5)

tk.Label(frame_formulario, text="Nivel de ejercicio:").grid(row=5, column=0, sticky="w")
entry_nivel_ejercicio = tk.Entry(frame_formulario)
entry_nivel_ejercicio.grid(row=5, column=1, pady=5)

# Botón para procesar el formulario
boton_enviar = tk.Button(frame_formulario, text="Enviar", command=procesar_formulario)
boton_enviar.grid(row=6, column=0, columnspan=2, pady=10)

# Frame para la página roja (inicialmente oculto)
frame_pagina_roja = tk.Frame(ventana, bg="#ffcccc")

# Ejecutar la ventana
ventana.mainloop()
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# que tenga la fecha "2000-03-15" y el usdpreice "0,804324", pero hay varias fechas y varios precios

def promediar_precios_por_fecha(df):
    """
    Agrupa el DataFrame por la columna 'date', calcula el promedio de 'price' para cada fecha,
    y devuelve un nuevo DataFrame con las fechas únicas y los precios promediados.
    
    Parámetros:
        df (pd.DataFrame): DataFrame con las columnas 'date' y 'price'.
        
    Retorna:
        pd.DataFrame: DataFrame con las fechas únicas y los precios promediados.
    """
    # Agrupar por 'date' y calcular el promedio de 'price'
    df_promedio = df.groupby("date", as_index=False)["usdprice"].mean()
    
    # Renombrar la columna de precio promediado
    df_promedio.rename(columns={'usdprice': 'usdprice_promedio'}, inplace=True)
    
    return df_promedio


def escalada_de_data(date):
    date = date.toordinal()
    scaler = StandardScaler()

# lists => list[str]
def regresorIngredientes(lists):

    ingredi_dict = {}
    
    #convertimos los ingredientes en minusculas
    lists = [str.lower(x) for x in lists]

    df = pd.read_csv("./dataset/wfp_food_prices_col.csv")
    #quitamos la primera fila de todas porque no es necesaria
    df.drop(0, inplace=True)
    
    #convertimos los commodity en minusculas y le quitamos todo lo que este dentro de "()"
    df["commodity"] = df["commodity"].str.lower()
    df["commodity"] = df["commodity"].str.replace(r'\(.*?\)', '', regex=True)
    #pasomos usdprice a float
    df['usdprice'] = pd.to_numeric(df['usdprice'])

    
    for ingrediente in lists:

        #Este bloque de codigo es para que cuando tengamos una para como "ovile oil", separarlos y agarra unicamente "oil"
        pla = ingrediente.split()
        for p in pla:
            df_ingre = df[df["commodity"].str.contains(p,regex=True)]       
            if(df_ingre.shape[0]==0):
                continue
            else:
                break
        
        if(df_ingre.shape[0]==0):

            ingredi_dict[ingrediente] = None
        else:
            df_ingre_pro = promediar_precios_por_fecha(df_ingre)
            
            df_ingre_pro['date'] = pd.to_datetime(df_ingre_pro['date'])

            X = df_ingre_pro[['date']].map(lambda x: x.toordinal())
            y = df_ingre_pro['usdprice_promedio']  # Variable objetivo
            
            # 4. Dividir los datos en conjuntos de entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)  # Ajustar y transformar el conjunto de entrenamiento
            X_test_scaled = scaler.transform(X_test)  # Transformar el conjunto de prueba (usando el mismo ajuste)

            model = LinearRegression()
            model.fit(X_train_scaled, y_train)  # Entrenar el modelo con los datos escalados
    
            ingredi_dict[ingrediente] = {"modelo" : model, "scaler" : scaler}
    
    return ingredi_dict
        

if __name__=="__main__":
    ho = ["flour", "salt", "cornmeal", "olive oil", "shortening", "cheddar cheese", "water", "eggs", "sugar", "butter", "flour", "buttermilk", "lemon zest", "lemon juice", "sugar"]
    fefe = regresorIngredientes(ho)

    print(fefe)
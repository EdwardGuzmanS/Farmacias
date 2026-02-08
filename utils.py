import requests
import pandas as pd

def cargar_datos(url):
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    # Normalizar nombres de farmacias
    df['local_nombre'] = df['local_nombre'].str.upper().str.strip()
    df['local_nombre'] = df['local_nombre'].replace({
        'CRUZ VERDE': 'CRUZ VERDE',
        'FARMACIA CRUZ VERDE': 'CRUZ VERDE',
        'AHUMADA': 'AHUMADA',
        'FARMACIAS AHUMADA': 'AHUMADA',
        'DR. SIMI': 'DR. SIMI',
        'DEL DR. SIMI': 'DR. SIMI'
    })
    return df

def mas_repetidos(df, column):
    return df[column].value_counts().head(5)

import matplotlib.pyplot as plt
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


#Obtención de los datos atraves de la pagina del gobierno https://datos.gob.cl/dataset/farmacias-en-chile
url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocales.php'
df = cargar_datos(url)

# Gráfico Top 5 comunas con más farmacias
top_comunas = mas_repetidos(df, 'comuna_nombre')
plt.figure(1, figsize=(5,5))
ax = top_comunas.plot(kind='bar', color='skyblue')
plt.title('Top 5 comunas con más farmacias')
plt.xlabel('Comuna')
plt.ylabel('Cantidad de farmacias')
plt.tight_layout()

# Agregar los valores encima de cada barra
for i, v in enumerate(top_comunas):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

plt.show()

# Gráfico Top 5 locales más reiterados
top_locales = mas_repetidos(df, 'local_nombre')
plt.figure(figsize=(5,5))
ax2 = top_locales.plot(kind='bar', color='orange')
plt.title('Top 5 locales más reiterados')
plt.xlabel('Local')
plt.ylabel('Cantidad de repeticiones')
plt.tight_layout()

# Agregar los valores encima de cada barra
for i, v in enumerate(top_locales):
    ax2.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')

plt.show()

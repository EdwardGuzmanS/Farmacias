import streamlit as st
import pandas as pd
import altair as alt
from utils import cargar_datos


#Creacion de stream lit
st.title("Dashboard de Farmacias en Chile")

#Obtención de los datos atraves de la pagina del gobierno https://datos.gob.cl/dataset/farmacias-en-chile
url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocales.php'

def mas_repetidos(df, column):
    return df[column].value_counts().head(5)

df = cargar_datos(url)

# Convertir latitud y longitud a tipo numérico
df['local_lat'] = pd.to_numeric(df['local_lat'], errors='coerce')
df['local_lng'] = pd.to_numeric(df['local_lng'], errors='coerce')

# Renombrar columnas para pydeck
df = df.rename(columns={
    'local_lat': 'lat',
    'local_lng': 'lon'
})

# Top 5 comunas
top_comunas = mas_repetidos(df, 'comuna_nombre').reset_index()
top_comunas.columns = ['comuna', 'cantidad']

# Definir las cadenas principales y colores
empresas_principales = {
    'ahumada': 'Ahumada',
    'cruz verde': 'Cruz Verde',
    'salcobrand': 'Salcobrand',
    'knop': 'Knop',
    'dr. simi': 'Dr Simi'
}
colores = {
    'Ahumada': '#E53935',      # Rojo
    'Cruz Verde': '#43A047',   # Verde
    'Salcobrand': '#1E88E5',   # Azul
    'Knop': '#FDD835',         # Amarillo
    'Dr Simi': '#8E24AA',      # Morado
    'Otras': '#BDBDBD'         # Gris
}

# Normalizar nombres
df['local_nombre'] = df['local_nombre'].str.lower().str.strip()
df['empresa'] = df['local_nombre'].map(empresas_principales).fillna('Otras')

# Agrupar por comuna y empresa
df_empresas = df.groupby(['comuna_nombre', 'empresa']).size().reset_index(name='cantidad')

# Filtrar solo las top 5 comunas
top_comunas_nombres = top_comunas['comuna'].tolist()
df_empresas_top = df_empresas[df_empresas['comuna_nombre'].isin(top_comunas_nombres)]

st.subheader("Distribución de farmacias en las top 5 comunas")

# Crear gráfico Altair
chart = alt.Chart(df_empresas_top).mark_bar().encode(
    y=alt.Y('comuna_nombre:N', title='COMUNA', sort=top_comunas_nombres),
    x=alt.X('cantidad:Q', title='CANTIDAD DE FARMACIAS'),
    color=alt.Color('empresa:N',
        scale=alt.Scale(domain=list(colores.keys()), range=list(colores.values())),
        legend=alt.Legend(title="FARMACIA")
    ),
    order=alt.Order('empresa', sort='descending'),
    tooltip=['comuna_nombre', 'empresa', 'cantidad']
).properties(height=300)

st.altair_chart(chart, use_container_width=True)

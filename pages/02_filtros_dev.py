import streamlit as st
import pandas as pd
from utils import cargar_datos

url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocales.php'
df = cargar_datos(url)
# Convertir las columnas de latitud y longitud a tipo numérico
df['local_lat'] = pd.to_numeric(df['local_lat'], errors='coerce')
df['local_lng'] = pd.to_numeric(df['local_lng'], errors='coerce')

st.title("Filtros Dev: Cantidad de Farmacias por Comuna y Empresa")

comuna_seleccionada = st.selectbox('Selecciona una comuna', df['comuna_nombre'].unique())
empresas_disponibles = df[df['comuna_nombre'] == comuna_seleccionada]['local_nombre'].unique()
empresa_seleccionada = st.multiselect('Selecciona empresas', empresas_disponibles)

# Filtrado por comuna y empresa
if empresa_seleccionada:
    filtro_df = df[
        (df['comuna_nombre'] == comuna_seleccionada) &
        (df['local_nombre'].isin(empresa_seleccionada))
    ]
else:
    filtro_df = df[df['comuna_nombre'] == comuna_seleccionada]

cantidad_farmacias = filtro_df.shape[0]
st.metric(label="Cantidad de farmacias", value=cantidad_farmacias)

st.dataframe(filtro_df)
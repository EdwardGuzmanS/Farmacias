import streamlit as st
from utils import cargar_datos, mas_repetidos
import pandas as pd

#Obtención de los datos atraves de la pagina del gobierno https://datos.gob.cl/dataset/farmacias-en-chile
url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocales.php'
df = cargar_datos(url)

top_comunas = mas_repetidos(df, 'comuna_nombre')
top_locales = mas_repetidos(df, 'local_nombre')

# Analisis de datos con Streamlit
st.title("Análisis de Datos de Farmacias en Chile")
st.write("Datos obtenidos desde la API pública del gobierno de Chile.")

st.write("Cantidad de farmacias en el dataset: ", df.shape[0])

st.subheader("Top 5 comunas con más farmacias")
st.bar_chart(top_comunas.head(5), x_label= 'Comuna', y_label='Cantidad de farmacias')

st.subheader("Top 5 cadenas farmacéuticas")
st.bar_chart(top_locales.head(5), x_label= 'Cadena', y_label='Cantidad de farmacias')

import streamlit as st
from utils import cargar_datos
import pandas as pd


url = 'https://midas.minsal.cl/farmacia_v2/WS/getLocales.php'
df = cargar_datos(url)
# Convertir las columnas de latitud y longitud a tipo numérico
df['local_lat'] = pd.to_numeric(df['local_lat'], errors='coerce')
df['local_lng'] = pd.to_numeric(df['local_lng'], errors='coerce')


st.title("Filtros Interactivos")
comuna_seleccionada = st.selectbox('Selecciona una comuna', df['comuna_nombre'].unique())

# Filtrado solo por comuna
filtro_df = df[df['comuna_nombre'] == comuna_seleccionada]

# Selección de farmacia específica (solo si hay resultados)
if not filtro_df.empty:
    farmacia_opciones = filtro_df['local_nombre'].unique()
    farmacia_elegida = st.selectbox('Selecciona una farmacia', farmacia_opciones)
    farmacia_df = filtro_df[filtro_df['local_nombre'] == farmacia_elegida]

    # Si hay más de una farmacia con el mismo nombre, seleccionar por dirección
    if len(farmacia_df) > 1:
        direcciones = farmacia_df['local_direccion'].unique()
        direccion_elegida = st.selectbox('Selecciona la dirección del local', direcciones)
        farmacia_df = farmacia_df[farmacia_df['local_direccion'] == direccion_elegida]

    farmacia_df = farmacia_df.rename(columns={
        'local_lat': 'lat',
        'local_lng': 'lon'
    })

    st.map(farmacia_df[['lat', 'lon']].dropna())
else:
    st.write("No hay farmacias disponibles para los filtros seleccionados.")

# Mostrar información general de la farmacia escogida
st.subheader("Información de utilidad de la farmacia seleccionada")
info = farmacia_df.iloc[0]  # tomar la primera fila

if info['local_nombre'] == 'CRUZ VERDE':
    st.image('pages/Cruz_Verde.jpg',width=300)
elif info['local_nombre'] == 'SALCOBRAND':
    st.image('pages/Salcobrand.jpeg',width=300)
elif info['local_nombre'] == 'AHUMADA':
    st.image('pages/Farmacias_Ahumada.png',width=300)
elif info['local_nombre'] == 'DR. SIMI':
    st.image('pages/dr_simi.png',width=300)
elif info['local_nombre'] == 'KNOP':
    st.image('pages/farmacia_knop.png',width=300)

st.write(f"""
**Dirección:** {info['local_direccion']}  
**Teléfono:** {info['local_telefono']}  
**Horario:** {info['funcionamiento_hora_apertura']} - {info['funcionamiento_hora_cierre']}  
**Comuna:** {info['comuna_nombre']}  
""")
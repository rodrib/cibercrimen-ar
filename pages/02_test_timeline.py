import streamlit as st
import pandas as pd

# pip install streamlit-vis-timeline
from streamlit_timeline import st_timeline # https://github.com/giswqs/streamlit-timeline?tab=readme-ov-file
from datetime import date, timedelta


# Cargar el archivo CSV directamente
csv_file_path = "cibercrimen-ar.csv"
df = pd.read_csv(csv_file_path)

# Adaptar el DataFrame, solo usando la columna 'Evento'
dfDatos = pd.DataFrame({
    "start": pd.to_datetime('today'),  # Usar la fecha actual como valor por defecto
    "end": pd.to_datetime('today'),  # Mismo valor para 'start' y 'end'
    "title": df['Evento'],  # Usar la columna 'Evento' como título
    "content": df['Descripcion'],  # Usar la columna 'Evento' también como contenido
    "color": None,
    "textcolor": None,
    "type": 'box'
})

# Rellenar valores NaN con cadenas vacías en las columnas 'title', 'content', 'color', 'textcolor'
dfDatos['title'] = dfDatos['title'].fillna('')
dfDatos['content'] = dfDatos['content'].fillna('')
dfDatos['color'] = dfDatos['color'].fillna('')
dfDatos['textcolor'] = dfDatos['textcolor'].fillna('')

# Convertir fechas a formato de cadena (str)
dfDatos['start'] = dfDatos['start'].dt.strftime('%Y-%m-%d')
dfDatos['end'] = dfDatos['end'].dt.strftime('%Y-%m-%d')

# Ajustar las fechas mínimas y máximas para la línea de tiempo
FechaMin = (pd.to_datetime(dfDatos["start"]).min() - timedelta(days=365)).strftime('%Y-%m-%d')
FechaMax = (pd.to_datetime(dfDatos["start"]).max() + timedelta(days=365)).strftime('%Y-%m-%d')

# Generar la línea de tiempo
st.header("Línea de tiempo de Cibercrimen")
timeline = st_timeline(dfDatos.to_dict('records'), groups=[], options={"min": FechaMin, "max": FechaMax}, height="600px")

# Mostrar detalles del evento seleccionado
if timeline:
    evento = dfDatos.iloc[timeline["id"]]
    detalleEvento = f"""
                    #### {evento['title']}
                    **Fecha**: {evento['start']}\n\n
                    {evento['content']}
    """
    st.write(detalleEvento, unsafe_allow_html=True)
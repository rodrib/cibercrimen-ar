import streamlit as st
import pandas as pd
from streamlit_timeline import st_timeline
from datetime import timedelta

# Cargar el archivo CSV directamente
csv_file_path = "cibercrimen-ar.csv"
df = pd.read_csv(csv_file_path)

# Verificar si existe una columna 'Año' o 'Fecha'
if 'Año' in df.columns:
    # Si el archivo tiene una columna de años
    df['start'] = pd.to_datetime(df['Año'], format='%Y', errors='coerce')
    df['end'] = df['start']  # Usamos el mismo año como fecha de inicio y fin
else:
    # Si hay una columna 'Fecha', usaremos esa
    df['start'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['end'] = df['start']

# Reemplazar NaT (valores inválidos o faltantes de fechas) por una fecha predeterminada
fecha_default = pd.to_datetime('2000-01-01')  # Puedes cambiar esta fecha por otra si lo prefieres
df['start'] = df['start'].fillna(fecha_default)
df['end'] = df['end'].fillna(fecha_default)

# Adaptar el DataFrame, usando las columnas 'Evento' y 'Descripcion'
dfDatos = pd.DataFrame({
    "start": df['start'],  # Usar la columna de fechas ajustada
    "end": df['end'],  # Usar la misma fecha para 'end'
    "title": df['Evento'],  # Usar la columna 'Evento' como título
    "content": df['Descripcion'],  # Usar la columna 'Descripcion' como contenido
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

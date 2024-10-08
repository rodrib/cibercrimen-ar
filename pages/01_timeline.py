import streamlit as st
import pandas as pd

# pip install streamlit-vis-timeline
from streamlit_timeline import st_timeline # https://github.com/giswqs/streamlit-timeline?tab=readme-ov-file
from datetime import date, timedelta

st.set_page_config(
    page_title="Generador de líneas de tiempo", #Título de la página
    page_icon="📊", # Ícono
    layout="wide", # Forma de layout ancho o compacto
    initial_sidebar_state="expanded" # Definimos si el sidebar aparece expandido o colapsado
)

# Creamos un panel expander para ocultar cuando se desee ver solo la línea de tiempo
with st.expander("Parámetros"):    
    st.header("Creador de líneas de tiempo")
    
    #Creamos dataframe base con los campos requeridos
    dfDatos = pd.DataFrame({"start":[None],"end":[None],'title':[None],"content":[None],"color":[None],"textcolor":[None],"type":[None]})    
    columnas =['start', 'end', 'title', 'content', 'color', 'textcolor', 'type']
    # Parámetro para el alto de la línea de tiempo
    parAltoTimeline = st.slider("Alto de gráfico",min_value=600,step=100,max_value=1800)
    # Parámetro para cargar líneas de tiempo ya creadas
    parArchivo = st.file_uploader("Archivo de línea de tiempo",type=['csv'])
    if parArchivo is not None:           
        # Se puede cargar con pandas si se tiene detectado el tipo de archivo
        if '.csv' in parArchivo.name:
            df = pd.read_csv(parArchivo,usecols=columnas)
        if len(df) > 0:
            df['start'] = pd.to_datetime(df['start'])
            df['end'] = pd.to_datetime(df['end'])
            dfDatos=df        
    # Parámetro para el título
    parTitulo = st.text_input("Titulo de la línea de tiempo")
    # Cargamos el data_editor que retorna un dataframe editable
    dfDatos=st.data_editor(dfDatos, #Dataframe base
            num_rows ="dynamic", # Indica que las columnas pueden aumentar dinámicamente
            use_container_width=True, # Indicamos que se adapte al ancho disponible
            column_config={ #Configuración personalizada de columnas
            "start": st.column_config.DateColumn(
                "start",            
                default=None,                    
                step=1,
                ),
            "end": st.column_config.DateColumn(
                "end",            
                default=None,            
                step=1,
                ),
            "type": st.column_config.SelectboxColumn(
                "type",            
                width="medium",
                default='box',
                options=[ 'box', 'point', 'range', 'background'],
                required=True,
            )
            },
            )
# Validamos que existan datos para generar la línea de tiempo
if len(dfDatos.dropna()) > 0: 
    items=[]
    if parArchivo:
        dfDatos['start'] = dfDatos['start'].dt.strftime('%Y-%m-%d')
        dfDatos['end'] = dfDatos['end'].dt.strftime('%Y-%m-%d')
    columns=dfDatos.columns
    item ={}
    
    # Recorremos el dataframe
    for indice, fila in dfDatos.iterrows():      
        item["style"]=""
        # Generamos los items para el array que se entrega al control
        # https://visjs.github.io/vis-timeline/docs/timeline/
        # Ejemplo:
        # items = [
        #     {"id": 1, "content": "2022-10-20", "start": "2022-10-20"},
        #     {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
        #     {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
        #     {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
        #     {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
        #     {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
        # ]
        for col in columns: 
            if fila[col]:
                if col == "color":
                    color=fila["color"]
                    item["style"]= f"background-color:{color};" + item["style"]
                elif col == "textcolor":
                    color =fila["textcolor"]
                    item["style"]= f"color:{color};" + item["style"]
                elif col == "title":
                    item["title"] =fila["start"]
                elif col=="content":
                    item["content"] =fila["title"]
                else:
                    item[col] = fila[col]                    
        item["id"] = indice # Adicionamos el id
        items.append(item) # Adicionamos el item al array
        item ={} # Reinicializamos la variable
    # Calculamos las fechas iniciales y finales
    FechaMin = (pd.to_datetime(dfDatos["start"]).min()+timedelta(days=-365)).strftime('%Y-%m-%d')
    FechaMax = (pd.to_datetime(dfDatos["start"]).max()+timedelta(days=365)).strftime('%Y-%m-%d')

    # Mostramos los resultados
    st.header(parTitulo)
    c1, c2 = st.columns([8,2])
    with c1:
        # Generamos la línea de tiempo retornando el valor seleccionado a la variable timeline
        timeline = st_timeline(items, groups=[], options={"min":FechaMin,"max":FechaMax,"align":"left"}, height=f"{parAltoTimeline}px",width="100%")    
    with c2:
        # Validamos si se seleccionó un evento
        if timeline:
            # Buscamos el evento con el id
            dfEvento =dfDatos.iloc[timeline["id"]]
            # Armamos el texto para mostrar
            detalleEvento = f"""
                            #### {dfEvento['title']}
                            **Fecha**: {dfEvento['start']}\n\n
                            {dfEvento['content']}
            """
            # Mostramos los detalles del evento seleccionado
            st.write(detalleEvento,unsafe_allow_html=True)


    ##### testando con el df

    # Cargar el archivo CSV en un DataFrame
df = pd.read_csv('cibercrimen-ar.csv')


#Convertir la columna 'Fechas' a datetime
df['Fechas'] = pd.to_datetime(df['Fechas'], errors='coerce', dayfirst=True)

# Extraer año y mes de la columna 'Fechas'
df['Año'] = df['Fechas'].dt.year
df['Mes'] = df['Fechas'].dt.month

st.dataframe(df)

######################

# Configuración de la página de Streamlit


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
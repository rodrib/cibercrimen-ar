import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px
import pandas as pd

# ---- MAINPAGE ----
st.title(":bar_chart: Ciberincidentes en Argentina")
st.markdown("##")


st.markdown("##")
st.markdown("Recopilación de los incidentes de ciberseguridad más importantes de Argentina que fueron publicados en medios. En algunos casos hay link a la Sanción de la Autoridad de Protección de datos. [@Marce_I_P en Twitter](https://twitter.com/Marce_I_P).")



# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('cibercrimen-ar.csv')


#Convertir la columna 'Fechas' a datetime
df['Fechas'] = pd.to_datetime(df['Fechas'], errors='coerce', dayfirst=True)

# Extraer año y mes de la columna 'Fechas'
df['Año'] = df['Fechas'].dt.year
df['Mes'] = df['Fechas'].dt.month

# Verificar que la columna 'Mes' contiene valores de 1 a 12
#st.write("Contenido de la columna 'Mes':")
#st.write(df['Mes'].unique())

# Crear una interfaz de usuario en Streamlit para seleccionar los años
anos_disponibles = df['Año'].dropna().unique().astype(int).astype(str)
anos_seleccionados = st.multiselect("Selecciona los Años para comparar", anos_disponibles, default=anos_disponibles)

# Filtrar los datos por los años seleccionados
df_filtrado = df[df['Año'].isin([int(ano) for ano in anos_seleccionados])]

# Contar la cantidad de eventos por año y mes
eventos_por_mes_ano = df_filtrado.groupby(['Año', 'Mes']).size().reset_index(name='Cantidad de Eventos')

# Crear un gráfico de líneas para mostrar los eventos por mes y año
fig = px.line(eventos_por_mes_ano, x='Mes', y='Cantidad de Eventos', color='Año',
              labels={'Mes': 'Mes', 'Cantidad de Eventos': 'Cantidad de Eventos'},
              title='Cantidad de Eventos por Mes y Año')

# Configurar el diseño del gráfico
fig.update_layout(
    xaxis=dict(
        tickmode="linear",
        tick0=1,
        dtick=1,
        title="Mes"
    ),
    yaxis=dict(
        title="Cantidad de Eventos",
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)"
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)


# Contar la cantidad de eventos por región
eventos_por_region = df_filtrado['Region'].value_counts().reset_index()
eventos_por_region.columns = ['Region', 'Cantidad de Eventos']

# # Crear un gráfico de barras para mostrar la cantidad de eventos por región
# fig = px.bar(eventos_por_region, x='Region', y='Cantidad de Eventos',
#              labels={'Region': 'Región', 'Cantidad de Eventos': 'Cantidad de Eventos'},
#              title='Cantidad de Eventos por Región')

# # Configurar el diseño del gráfico
# fig.update_layout(
#     xaxis=dict(
#         title="Región"
#     ),
#     yaxis=dict(
#         title="Cantidad de Eventos",
#         showgrid=False
#     ),
#     plot_bgcolor="rgba(0,0,0,0)"
# )

# # Mostrar el gráfico en Streamlit
# st.plotly_chart(fig, use_container_width=True)

########
import plotly.graph_objects as go

# Crear un gráfico de barras con bordes redondeados
fig = go.Figure(data=[
    go.Bar(
        x=eventos_por_region['Region'],
        y=eventos_por_region['Cantidad de Eventos'],
        marker=dict(
            line=dict(color='rgba(0,0,0,0)'),
            color='rgba(0, 123, 255, 0.6)',
            opacity=0.8
        ),
        width=0.5,  # Adjust the width of the bars
        marker_line_width=0,  # Set the marker line width to 0
        marker_line_color='rgba(0,0,0,0)',  # Set the marker line color to transparent
        text=eventos_por_region['Cantidad de Eventos'],  # Display the values on top of the bars
        textposition='outside'
    )
])

# Actualizar el layout para agregar bordes redondeados
fig.update_traces(
    marker=dict(
        line=dict(width=1.5, color='black'),
        color='rgba(0, 123, 255, 0.6)',
        opacity=0.8
    )
)

# Configurar el diseño del gráfico
fig.update_layout(
    title='Cantidad de Eventos por Región',
    xaxis=dict(
        title="Región"
    ),
    yaxis=dict(
        title="Cantidad de Eventos",
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)"
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

########## Grafico verde
# import streamlit as st

# # Especificación de Vega-Lite
# vega_lite_spec = {
#     "mark": {"type": "bar", "tooltip": True, "fill": "rgb(173, 250, 29)", "cornerRadiusEnd": 4},
#     "encoding": {
#         "x": {"field": "Region", "type": "ordinal"},
#         "y": {"field": "Cantidad de Eventos", "type": "quantitative", "axis": {"grid": False}},
#     },"title": "Cantidad de Eventos por Región"  # Título del gráfico
# }

# # Renderizar el gráfico utilizando st.vega_lite_chart()

# st.vega_lite_chart(eventos_por_region.reset_index(), vega_lite_spec, use_container_width=True)


###############
# Tipos de Evento

# Contar la cantidad de eventos por tipo
eventos_por_tipo = df['Tipo'].value_counts().reset_index()
eventos_por_tipo.columns = ['Tipo de Evento', 'Cantidad de Eventos']

# Crear un gráfico de barras con bordes redondeados
fig = go.Figure(data=[
    go.Bar(
        x=eventos_por_tipo['Tipo de Evento'],
        y=eventos_por_tipo['Cantidad de Eventos'],
        marker=dict(
            line=dict(color='rgba(0,0,0,0)'),
            color='rgba(255, 0, 0, 0.6)',  # Color rojo con 60% de opacidad
            opacity=0.8
        ),
        width=0.5,  # Ajustar el ancho de las barras
        marker_line_width=0,  # Establecer el ancho de la línea del marcador a 0
        marker_line_color='rgba(0,0,0,0)',  # Establecer el color de la línea del marcador a transparente
        text=eventos_por_tipo['Cantidad de Eventos'],  # Mostrar los valores en la parte superior de las barras
        textposition='outside'
    )
])

# Actualizar el layout para agregar bordes redondeados
fig.update_traces(
    marker=dict(
        line=dict(width=1.5, color='black'),
        color='rgba(255, 0, 0, 0.6)',  # Color rojo con 60% de opacidad
        opacity=0.8
    )
)

# Configurar el diseño del gráfico
fig.update_layout(
    title='Distribución de Tipos de Eventos',
    xaxis=dict(
        title="Tipo de Evento"
    ),
    yaxis=dict(
        title="Cantidad de Eventos",
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)"
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)


#########
# Contar la cantidad de eventos por programa
eventos_por_programa = df['Programa'].value_counts().reset_index()
eventos_por_programa.columns = ['Programa', 'Cantidad de Eventos']

# Crear un gráfico de barras con bordes redondeados
fig = go.Figure(data=[
    go.Bar(
        x=eventos_por_programa['Programa'],
        y=eventos_por_programa['Cantidad de Eventos'],
        marker=dict(
            line=dict(color='rgba(0,0,0,0)'),
            color='rgba(0, 255, 0, 0.6)',  # Color verde con 60% de opacidad
            opacity=0.8
        ),
        width=0.5,  # Ajustar el ancho de las barras
        marker_line_width=0,  # Establecer el ancho de la línea del marcador a 0
        marker_line_color='rgba(0,0,0,0)',  # Establecer el color de la línea del marcador a transparente
        text=eventos_por_programa['Cantidad de Eventos'],  # Mostrar los valores en la parte superior de las barras
        textposition='outside'
    )
])

# Actualizar el layout para agregar bordes redondeados
fig.update_traces(
    marker=dict(
        line=dict(width=1.5, color='black'),
        color='rgba(0, 255, 0, 0.6)',  # Color verde con 60% de opacidad
        opacity=0.8
    )
)

# Configurar el diseño del gráfico
fig.update_layout(
    title='Cantidad de Eventos por Programa',
    xaxis=dict(
        title="Programa"
    ),
    yaxis=dict(
        title="Cantidad de Eventos",
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)"
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)


##############
import streamlit as st
import calplot

# Imprimir las columnas de fechas en Streamlit
#st.write(df["Fechas"])



import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



#configuracion página

st.set_page_config(page_title="Dashboard",
                   page_icon= '\U0001F4CA',
                   layout="wide")


st.title("\U0001F4CA Data visualization Dashboard")
st.markdown('### Explorando diferentes bibliotecas de visualización en Python')

#Introducción
with st.expander('Introducción', expanded=True):
    st.markdown('''
    Esta aplicaciión demuestra el uso de difrentes bibliot4ecas de visialización Python:
    * **Matplotlib* Biblioteca base pra visualización
    * **Seaborn* Visualizaciones estadisticas alto nivel
    * **Streamlit* Framework para aplicaciones de datos
    ''')

try:

    #cargamos los datos de peliculas de netfilx

    prog_df = pd.read_csv(os.path.join(BASE_DIR, 'Data/netflix_titles.csv'))
    prog_df = prog_df[prog_df["type"].str.contains("Movie")]
    #prog_df['dur_minutos'] = prog_df["duration"].str.replace("min", "", regex=False).str.strip().astype(str)

    prog_df["dur_minutos"] = (
        prog_df["duration"]
        .astype(str)  # convierto todo a string
        .str.extract(r"(\d+\.?\d*)")  # extraigo solo números
        .astype(int)  # convierto a float
    )

    prog_df_gr = prog_df.groupby('dur_minutos')['country'].count().reset_index(name='conteo_dur_min')
    #st.dataframe(prog_df_gr)
    prog_df_gr_top10 = prog_df_gr.sort_values(by=['dur_minutos'], ascending=False).head(10)
    st.dataframe(prog_df_gr_top10)

    #Cargo el nuevo de IMDB
    df_imbd = pd.read_csv(os.path.join(BASE_DIR, 'Data/imdb_top_1000.csv'))
    st.info(df_imbd)




    iris_df = pd.read_csv(os.path.join(BASE_DIR, 'Data/Iris.csv'))
    st.success('\U0001F4DA Datos cargados')


    st.header('Visualizaciones con Matplotlib')

    with st.container():
        col1 , col2 = st.columns(2)
        with col1:
            st.subheader('Grafico de dispersion')
            fig, ax = plt.subplots(figsize=(8,6))
            x = prog_df_gr['dur_minutos']#.head(100)
            y = prog_df_gr['conteo_dur_min']#.head(100)
            st.write('entro la y')
            ax.scatter(x,y, color='green', alpha=0.6) #alpha es la opacidad
            plt.xticks(rotation=45) #orientacion etiquetas
            plt.title('cantidad de peliculas vs Duracion')
            plt.xlabel('duracion (min)')
            plt.ylabel('cuantas con esa duracion (peliculas)')
            st.pyplot(fig) #dibuja el gráfico
            plt.close()

        with col2:
            st.subheader('Grafico de barras')
            fig, ax = plt.subplots(figsize=(8,6))
            x = prog_df_gr['dur_minutos']#.head(100)
            y = prog_df_gr['conteo_dur_min']  # .head(100)
            ax.bar(x, y, color='skyblue', alpha=0.6)  # alpha es la opacidad
            plt.xticks(rotation=45)  # orientacion etiquetas
            plt.title('cantidad de peliculas vs Duracion')
            plt.xlabel('duracion (min)')
            plt.ylabel('cuantas con esa duracion (peliculas)')
            st.pyplot(fig)  # dibuja el gráfico
            plt.close()
        with col2:
            st.subheader('Grafico de Barras')

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Grafico de Violin')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.violinplot(data=iris_df, x='Species', y ='SepalLengthCm')
            plt.xticks(rotation=45)
            plt.title('Districión de longiud del sepalo por especie')
            st.pyplot(fig)
            plt.close()
        with col2:
            st.subheader('Grafico de Violin')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(data=iris_df, x='Species', y ='SepalLengthCm')
            plt.xticks(rotation=45)
            plt.title('Districión de longiud del sepalo por especie')
            st.pyplot(fig)
            plt.close()


    #visualización interactiva con Plotly
    st.header('Visualizaciones interactivas con Plotly')
    with st.container():
        #Grafico de lineas interactivo
        fig = px.line(prog_df_gr,
                      x='dur_minutos',
                      y='conteo_dur_min',
                      title='Minutos de pelis',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)

    #grafico de quesitos
    st.header('Visualizaciones interactivas con Plotly')
    with st.container():
        #Grafico de lineas interactivo
        fig = px.pie(prog_df_gr_top10,
                  values='dur_minutos',
                  names='conteo_dur_min',
                  title='Minutos de pelis')
        st.plotly_chart(fig, use_container_width=True)

    # 6 seccion interactiva
    st.header('\U0001F504 Seccion Interactiva')

    #selector de dataset
    dataset_choice = st.radio(
        'Selecciona el conjunto de datos',
        ['Pelis Netflix', 'Iris Dataset' , 'IMDB']
    )

    if dataset_choice == 'Pelis Netflix':
        df = prog_df
    elif dataset_choice == 'IMDB':
        df = df_imbd
    else:
        df = iris_df

    #selecionar la visualización
    chart_type = st.selectbox(
        'Selecciona el tipo de gráfico',
        ['Barras', 'Dispersion', 'Línea']
    )

    #selector de datos
    x_axis = st.selectbox('Selecciona el eje X', df.columns)
    y_axis = st.selectbox('Selecciona el eje Y', df.columns)

    #generar gráfico
    if chart_type == 'Barras':
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == 'Dispersion':
        fig = px.scatter(df, x=x_axis, y=y_axis)
    else:
        fig = px.line(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig, use_container_width=True)

    st.header(' Conclusiones')
    st.markdown('''
    Comparación de bibliotecas
    
    1. **Matplotlib**
    * Biblioteca base para visualización
    * Mayor control sobre controles del gráfico
    * Curva de aprendizaje mas pronunciada
    
    2. **Seaborn**
    * Construida sobre Matplotlib
    * Excelente para visualización de estadisticas
    * Estilos predefinidos atractivos
    
    3. **Streamlit**
    * Facilita la creació nde aplicaciones web
    * Integraación prefecta de otras bibliotecas
    * Desarrollo rápido de prototipos   
    ''')

    #footer
    st.markdown('------')















except Exception as e:
    st.error(f'\U0001F4DA Error {e}')


















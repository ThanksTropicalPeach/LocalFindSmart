import requests
from bs4 import BeautifulSoup
import pandas as pd

def obtener_datos_locales(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Listas para almacenar los datos extraídos
    titulos, precios, enlaces, ubicaciones = [], [], [], []

    # Extracción de los contenedores de cada publicación
    publicaciones = soup.find_all('div', class_='Col-sc-14ninbu-0.lfGZKA.col-md-8.col-lg-9')
    
    sc-ckVGcZ cFCiUO font-weight-light card-title
    
    for publicacion in publicaciones:
        # Título del anuncio
        if publicacion.find('h3',class_='sc-ckVGcZ cFCiUO font-weight-light card-title'):
            titulo = publicacion.find('h3',class_='sc-ckVGcZ cFCiUO font-weight-light card-title').get_text()
            titulos.append(titulo)
        else:
            titulo = publicacion.find('h2', class_='sc-dxgOiQ BSoGx card-title').get_text()
            titulos.append(titulo)
"""
        # Precio del local
        precio = publicacion.find('span', class_='andes-money-amount').get_text()
        precios.append(precio)

        
        enlace = publicacion.find('h2', class_='poly-box poly-component__title')
        link = enlace.find('a')['href']
        enlaces.append(link)
        

        # Ubicación del local
        ubicacion = publicacion.find('span', class_='poly-component__location').get_text()
        ubicaciones.append(ubicacion)
"""
    # Creación de DataFrame
    datos = pd.DataFrame({
        'Título': titulos,
        """'Precio': precios,
        'Ubicación': ubicaciones,
        'Enlace': enlaces"""
    })

    return datos

#iterar paginas
numeros=[]
dataframes=[]
response = requests.get('https://www.metrocuadrado.com/locales/arriendo/bogota/')
soup = BeautifulSoup(response.content, 'html.parser')
page_iterator=soup.find_all('li',class_='page-item')
for page in page_iterator: 
    numero= page.find('a').get_text()
    if numero.isdigit():
        url = page.find('a')['href']
        datos_locales = obtener_datos_locales(url)
        dataframes.append(datos_locales)
df_final = pd.concat(dataframes, ignore_index=True)

df_final.to_csv('locales_bogota_m2.csv', index=False, encoding='utf-8')

import streamlit as st
import pandas as pd

# Importa los datos del scraper (suponiendo que tienes los datos en un archivo CSV)
def cargar_datos():
    return pd.read_csv('locales_bogota_m2.csv')

st.title("Locales en arriendo en Bogotá")
st.markdown("Esta aplicación muestra los resultados de arriendos en Bogotá obtenidos de MercadoLibre.")

# Cargar los datos
datos = cargar_datos()

# Mostrar una tabla con los resultados
st.dataframe(datos)

# Filtros de búsqueda por precio o ubicación
rango_precio = st.slider("Selecciona un rango de precios", 0, 10000000, (500000, 5000000))
ubicacion = st.selectbox("Filtrar por ubicación", datos['Ubicación'].unique())

datos['Precio'] = datos['Precio'].replace({'\$': '', '\.': '', ',': ''}, regex=True).astype(int)
# Aplicar filtros
datos_filtrados = datos[
    (datos['Precio'].astype(int).between(*rango_precio)) &
    (datos['Ubicación'] == ubicacion)
]

st.subheader("Resultados filtrados")
st.dataframe(datos_filtrados)

# Mostrar enlaces a las publicaciones originales
for index, row in datos_filtrados.iterrows():
    st.write(f"[{row['Título']}]({row['Enlace']}) - ${row['Precio']}")
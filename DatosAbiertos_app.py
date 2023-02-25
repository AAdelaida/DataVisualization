#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[ ]:


# Dar formato a los datos
def formatea_data(data, columns):
    meses = {'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12}
    df = data.drop([0,1,2,3,4], axis=0)
    df.dropna()
    df = df[data['Unnamed: 2'].notna()]
    df.columns = columns
    df['Año'] = df['Año'].astype(str).str.replace('.00', '')
    df['Mes_num'] = df['Mes'].map(meses)
    df['Fecha'] = pd.to_datetime(df['Año'] + '-' + df['Mes_num'].astype(str) + '-01', format='%Y-%m-%d')
    df = df.drop(['Año', 'Mes', 'Mes_num'], axis=1)
    df["Año"] = pd.to_datetime(df.Fecha).dt.year
    df.set_index(
        pd.PeriodIndex(pd.to_datetime(df.Fecha), freq="M"),
        inplace= True,
    )
    return df

def formatea_padronRFC(data, columns):
    df = data.drop([0,1,2,3,4], axis=0)
    df.dropna()
    df = df[data['Unnamed: 3'].notna()]
    for i in range(3,24):
        df["Unnamed: " + str(i)] = df["Unnamed: " + str(i)].astype(float)
    df.columns = columns
    df['Año'] = df['Año'].astype(str).str.replace('.00', '')
    df["Año"] = pd.to_datetime(df.Año).dt.year
    return df


# In[ ]:


# Cargar archivo de datos de Facturas Electrónicas
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/FacEleNumCom.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10'], axis=1)
columns = ["Año", "Mes", "CompEmitidos", "AcumAnual", "AcumTotal"]
df_comprobantes = formatea_data(data, columns)


# In[ ]:


# Cargar archivo de datos de Emisores de Facturas Electrónicas
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/FacEleNumEmi.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 7'], axis=1)
columns = ["Año", "Mes", "Emisores", "AcumAnual", "AcumTotal"]
df_emisores = formatea_data(data, columns)


# In[ ]:


# Cargar archivo de datos de Inscripciones al RFC
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/InscTipContRFC.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'], axis=1)
columns = ["Año", "Mes", "PF", "PM", "Total"]
df_inscripciones = formatea_data(data, columns)


# In[ ]:


# Cargar archivo de datos de Suspenciones en el RFC
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/SusTipContRFC.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'], axis=1)
columns = ["Año", "Mes", "PF", "PM", "Total"]
df_suspensiones = formatea_data(data, columns)


# In[ ]:


# Cargar archivo de datos de Cancelaciones en el RFC
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/CancTipContRFC.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'], axis=1)
columns = ["Año", "Mes", "PF", "PM", "Total"]
df_cancelaciones = formatea_data(data, columns)


# In[ ]:


# Cargar padron de contribuyentes activos por Sector Económico
url = 'https://wu1aqauatsta002.blob.core.windows.net/datosabiertos/SectorActEco.csv'
data = pd.read_csv(url, encoding='latin1').drop(['Unnamed: 0', 'Unnamed: 2'], axis=1)
columns = ["Año", 
           "Actividades del gobierno y de organismos internacionales y extraterritoriales",
           "Agricultura, ganadería, aprovechamiento forestal, pesca y caza",
           "Comercio al por mayor",
           "Comercio al por menor", 
           "Construcción",
           "Dirección de corporativos y empresas",
           "Electricidad, agua y suministro de gas por ductos al consumidor final",
           "Industrias manufactureras",
           "Información en medios masivos",
           "Minería",
           "Otros",
           "Otros servicios excepto actividades del gobierno",
           "Servicios de alojamiento temporal y de preparación de alimentos y bebidas",
           "Servicios de apoyo a los negocios y manejo de desechos y servicios de remediación",
           "Servicios de esparcimiento culturales y deportivos, y otros servicios recreativos",
           "Servicios de salud y de asistencia social",
           "Servicios educativos",
           "Servicios financieros y de seguros",
           "Servicios inmobiliarios y de alquiler de bienes muebles e intangibles",
           "Servicios profesionales, científicos y técnicos",
           "Transportes, correos y almacenamiento",
          ]
df_contribuyentesActivos = formatea_padronRFC(data, columns)
df_contribuyentesActivos.head()


# In[ ]:


# Dar formato a los datos que se van a Visualizar
df_comprobantes["CompEmitidos"] = df_comprobantes["CompEmitidos"].astype(float)
df_emisores["Emisores"] = df_emisores["Emisores"].astype(float)
df_inscripciones["Total"] = df_inscripciones["Total"].astype(float)
df_suspensiones["Total"] = df_suspensiones["Total"].astype(float)
df_cancelaciones["Total"] = df_cancelaciones["Total"].astype(float)


# In[ ]:


# Establecer los valores predeterminados de Matplotlib
plt.style.use("seaborn-whitegrid")
plt.rc("figure", autolayout=True, figsize=(11,4))
plt.rc("axes", labelweight="bold", labelsize="large", titleweight="bold", titlesize=16, titlepad=10)
plot_params=dict(color="0.75", style=".-", markeredgecolor="0.25", markerfacecolor="0.25")


# In[ ]:


# Generar Tablero
st.title('Visualización de Datos Abiertos SAT')

st.sidebar.header('Fuente de Información: ')
st.sidebar.markdown("""
Sitio oficial de Datos Abiertos del Gobierno de México, el cual publica datos con las características técnicas 
y legales necesarias para que cualquiera, en cualquier lugar y momento, los pueda usar, reusar y distribuir libremente.

Aquí [https://datos.gob.mx](!https://datos.gob.mx) podrás descargar en formato libre todos los datos abiertos del Gobierno,
estados, municipios y órganos autónomos que han decidido sumarse para incrementar el beneficio de abrir información pública.
""")

# Selector de años
años = [2011,2012,2013,2014,2015,2016,2017,2018, 2019,2020,2021,2022,2023]
años_seleccionados = st.sidebar.multiselect('Años', años, años)

# Filtrar datos
df_comprobantes_seleccionados = df_comprobantes[(df_comprobantes.Año.isin(años_seleccionados))]
df_emisores_seleccionados = df_emisores[(df_emisores.Año.isin(años_seleccionados))]
df_inscripciones_seleccionados = df_inscripciones[(df_inscripciones.Año.isin(años_seleccionados))]
df_suspensiones_seleccionados = df_suspensiones[(df_suspensiones.Año.isin(años_seleccionados))]
df_cancelaciones_seleccionados = df_cancelaciones[(df_cancelaciones.Año.isin(años_seleccionados))]


# Filtrar datos padrón RFC
df_contribuyentesActSeleccionados = df_contribuyentesActivos[(df_contribuyentesActivos.Año.isin([2022]))]
df_contribuyentesActSeleccionados = df_contribuyentesActSeleccionados.drop("Año", axis=1)

st.markdown("""Contribuyentes activos por Sector Económico""")

# Generar gráfica padrón de contribuyentes
if not df_contribuyentesActivos.empty:
    fig, ax = plt.subplots(figsize=(26, 16))
    sns.barplot(data=df_contribuyentesActSeleccionados, orient="h")
    ax.set_yticklabels(df_contribuyentesActSeleccionados.columns.values, fontdict = {'fontsize': 30})
    st.pyplot(fig)


st.markdown("""Movimientos al RFC por año (***información disponible a partir de 2015***)""")

# Generar gráfica de movimientos al RFC
if not df_inscripciones_seleccionados.empty:
    fig, ax = plt.subplots()
    ax = df_inscripciones_seleccionados.Total[df_inscripciones_seleccionados.index].plot(color='tab:blue', marker='o', linestyle='solid',
     linewidth=2, markersize=3, ax=ax)
    ax = df_suspensiones_seleccionados.Total[df_suspensiones_seleccionados.index].plot(color='tab:green', marker='o', linestyle='solid',
     linewidth=2, markersize=3, ax=ax)
    ax = df_cancelaciones_seleccionados.Total[df_cancelaciones_seleccionados.index].plot(color='tab:orange', marker='o', linestyle='solid',
     linewidth=2, markersize=3, ax=ax)
    _ = ax.legend(['Inscripciones','Suspensiones', 'Cancelaciones'])
    st.pyplot(fig)

st.markdown("""Facturas Electrónicas Emitidas por año""")

# Generar gráficas de Factura Electrónica
if not df_comprobantes_seleccionados.empty:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6))
    ax1 = df_comprobantes_seleccionados.CompEmitidos[df_comprobantes_seleccionados.index].plot(color='tab:orange', marker='o', linestyle='solid',
     linewidth=2, markersize=3, ax=ax1)
    ax2 = df_emisores_seleccionados.Emisores[df_emisores_seleccionados.index].plot(color='tab:blue', marker='o', linestyle='solid',
     linewidth=2, markersize=3, ax=ax2)
    _ = ax1.legend(['Facturas Electrónicas'])
    _ = ax2.legend(['Emisores'])
    st.pyplot(fig)
    


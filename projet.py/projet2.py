from re import T
import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import plotly_express as px
import datetime as dt
from streamlit.elements.color_picker import ColorPickerMixin
import plotly_express as px
import plotly.graph_objects as go
import seaborn as sns
import time
import os
from PIL import Image 
import pydeck as pdk
import plotly.graph_objects as go



@st.cache()
def loadDF():
    df =  pd.read_csv("streamlit_project/projet.py/full_2020_17.csv")
    return df

df = loadDF()

req_col=['date_mutation','nature_mutation','valeur_fonciere','code_postal','nom_commune','type_local','surface_reelle_bati','nombre_pieces_principales','nature_culture','surface_terrain','longitude','latitude']
df = pd.read_csv("full_2020_17.csv",usecols=req_col,parse_dates=['date_mutation'],dtype={("nature_mutation ","nom_commune","nature_culture"):"category",("valeur_fonciere","surface_relle_bati","nombre_pieces_principales","surface_terrain","longitude","latitude","code_postal") : "float32"})
df['date_mutation']=pd.to_datetime(df["date_mutation"])

def get_month(df):
    return df.month

def dropage(df):
    df.dropna(axis=0, inplace=True)


def renaming(df,column1,column2):
        df.rename(columns={column1:column2},inplace=True)



dropage(df)
renaming(df,'valeur_fonciere','valeur_fonciere2020')
df['month']=df['date_mutation'].map(get_month)
mean_vf_2020=df.groupby('month').valeur_fonciere2020.mean()

@st.cache()
def loadDF_sansParis(df):
    dfSP =  df.loc[~df['nom_commune'].str.contains("Paris", case=False)]
    dfSP =  dfSP.loc[dfSP['valeur_fonciere2020'] <= 100000]
    dfSP =  dfSP.loc[dfSP['nature_mutation'].str.contains("Vente", case=False)]
    dfSP =  dfSP.loc[dfSP['surface_terrain'] > 9]
    dfSP =  dfSP.loc[dfSP['type_local'] == 'Maison']
    return dfSP

dfSP = loadDF_sansParis(df)

@st.cache()
def loadDF_Paris(df):
    dfSP =  df.loc[df['nom_commune'].str.contains("Paris", case=False)]
    dfSP =  dfSP.loc[dfSP['nature_mutation'].str.contains("Vente", case=False)]
    dfSP =  dfSP.loc[dfSP['type_local'] == 'Maison']
    return dfSP

dfAP = loadDF_Paris(df)

@st.cache()
def df42(df):
    df =  df.loc[df['longitude'].isin([*42])]
    

    return df

date = dt.date(2020,1,1)

dflight= df.sample(frac=0.25, replace=True, random_state=1)


#CHOIX DU DASHBOARD
st.sidebar.title("Choix du DashBoard")
option = st.sidebar.selectbox('Veuillez faire un choix',('Acceuil','Prix Immobilié à Paris','Numéro 42',))
st.header(option)

#########################################################
#DASH BOARD 1

def pageAcceuil():
    st.text('Noirclerc Thomas')
    st.title("Bienvenue dans la DashBoard d'analyse de donnée immobiliaire en 2020")
    st.text("Dans ce DashBoard vous retrouverai différents éléments pour visualiser des données \n immobilières en France en 2020")
    #Pour ecploiter des images 
    img = Image.open("acceuil_immeuble.jpeg") 
    st.image(img, width=700) 

    st.text("Voici le DataFrame utilisé, pour une plus simple utilisation, nous avons décidé de \nn'utiliser que 50 pourcent de la donnée disponible et ceci de façon aléatoire")
    st.text("Le dataframe ci-dessous que vous pouvez apercevoir est un dataframe fait avec des \nvaleurs aléatoires de 50 poucents de 'full_2020.cvs', \nil a été enregistré dans 'full_2020_2.csv' grâce au fichier df_random_50.py.")
    st.write(df.head(100000))

    st.title("Dash board 1 : ")
    st.text("Dans ce premier dashboard vous retrouverez tous les biens supérieurs à 9m2 et inférieur à 100 000 milles euros, \n (cela représente le prix moyen d'un bien à Paris pour 9m2) ")
    img = Image.open("11208669.jpeg") 
    st.image(img, width=700)

    st.title("Dash board 2 : ")
    st.text("Dans ce deuxième dashboard vous retrouverez tous les biens avec le numéro 42 dans leurs ligne, car on sait bien que 42 est la clés de l'univers) ")
    img = Image.open("reponse-42.jpeg") 
    st.image(img, width=700)


if option == 'Acceuil':
    pageAcceuil()

#########################################################
#DASH BOARD 2
def neufMetre():
    st.title("Bienvenue dans le Deuxième DashBoard")
    st.text("Dans ce DashBoard vous retrouverai différents éléments pour visualiser des biens mieux qu'à Paris !!! ")
    st.text("Voici le dashboard que nous allons utiliser : ")

    st.text("Voici le DataFrame utilisé, pour une plus simple utilisation, nous avons décidé de \nn'utiliser que 50 pourcent de la donnée disponible et ceci de façon aléatoire")
    st.text("Le dataframe ci-dessous que vous pouvez apercevoir est un dataframe fait avec des \nvaleurs aléatoires de 50 poucents de 'full_2020.cvs', \nil a été enregistré dans 'full_2020_2.csv' grâce au fichier df_random_50.py.")
    st.write(dfSP.head(100000))

    dfSP2 = dfSP.sample(frac=0.50, replace=True, random_state=1)
    st.write("#")
    st.write("#")
    st.subheader("Voici '50%' (des) des biens disponibles en 2020 en France à 100 000euros et à plus de 9m2 dans une carte : ")
    st.write("#")
    st.write("#")
    

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=46.227638,
            longitude=2.213749,
            zoom=6,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=dfSP2,
                get_position='[longitude, latitude]',
                radius=2000,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=dfSP2,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=2000,
            ),
        ],
    ))

    st.write("#")
    st.write("#")

    def Scatterplot():
        A,B = st.columns(2)
        axeX = A.radio("L'axe des X : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        axeY = B.radio("L'axe des y : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        plot = px.scatter(dfSP.head(200),x = axeX, y = axeY)
        plot2 = px.scatter(dfAP.head(200),x = axeX, y = axeY)
        st.title(f"Voici le Scatterplot du Dataframe sans Paris et seulement Paris de la {axeX}, en fonction de la {axeY} ")
        st.plotly_chart(plot)
        st.plotly_chart(plot2)
    
    def Lineplots():
        A,B = st.columns(2)
        axeX = A.radio("L'axe des X : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        axeY = B.radio("L'axe des y : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        line = px.line(dfSP.head(200),x = axeX, y = axeY)
        line2 = px.line(dfAP.head(200),x = axeX, y = axeY)
        st.title(f"Voici le Lineplot du Dataframe sans Paris et seulement Paris de la {axeX}, en fonction de la {axeY}")
        st.text("(c'est jolies mais pas très utiles)")
        st.plotly_chart(line)
        st.plotly_chart(line2)

    def Histogram():
        axeX = st.radio("L'axe des X : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        histogram_slider = st.sidebar.slider("Nombre de bins",min_value=5,max_value=100,value=30)
        fig = sns.displot(dfSP[axeX],bins = histogram_slider)
        fig2 = sns.displot(dfAP[axeX],bins = histogram_slider)
        st.title(f"Voici l'Histogram de du Dataframe sans Paris et seulement Paris en fonction de la {axeX}")
        st.pyplot(fig)
        st.pyplot(fig2)
    
    def Boxplot():
        A,B = st.columns(2)
        axeX = A.radio("L'axe des X : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        axeY = B.radio("L'axe des y : ", ('longitude','latitude','valeur_fonciere2020','surface_terrain','nom_commune'))
        boxe = px.box(dfSP.head(10),x = axeX, y = axeY)
        boxe2 = px.box(dfAP.head(10),x = axeX, y = axeY)
        st.title(f"Voici le Boxplot du Dataframe sans Paris et seulement Paris de la {axeX}, en fonction de la {axeY}")
        st.plotly_chart(boxe)
        st.plotly_chart(boxe2)


    option = st.radio(('Choisis votre chart'),('Scatterplot','Lineplots','Histogram','Boxplot'))

    
    if option == 'Scatterplot' :
        Scatterplot()
    if option == 'Lineplots':
        Lineplots()    
    if option == 'Histogram':
        Histogram()
    if option == 'Boxplot':
        Boxplot()

    
    #def Boxplot():

if option == 'Prix Immobilié à Paris' :
    neufMetre()

#########################################################
#DASH BOARD 3
def numero42():
    st.title("Bienvenue dans le Deuxième DashBoard sur le thème du nombre 42")
    st.text("°  ___  _____              ___  _____              ___  _____              ___  _____\n  /   |/ __  \            /   |/ __  \            /   |/ __  \            /   |/ __  \ \n / /| |`' / /'           / /| |`' / /'           / /| |`' / /'           / /| |`' / /'\n/ /_| |  / /            / /_| |  / /            / /_| |  / /            / /_| |  / /\n\___  |./ /___          \___  |./ /___          \___  |./ /___          \___  |./ /___\n    |_/\_____/              |_/\_____/              |_/\_____/              |_/\_____/")
    
    st.text("Dans ce scatter plot par exemple vous retrouverez tous les biens de France \n avec une valeur foncière de 420000 max et de taille de terrain 42000m2 :")
    
    def first42chart():
        fig = px.scatter(dflight, x="valeur_fonciere2020", y="surface_terrain", animation_group="nom_commune",
            log_x=True, size_max=55, range_x=[42,420000], range_y=[42,42000])

        fig["layout"].pop("updatemenus") # optional, drop animation buttons
        st.plotly_chart(fig)

        fig = go.Figure()
    
    first42chart()

    st.text("°     44    2222                   44    2222                   44    2222\n     444   222222                 444   222222                 444   222222\n   44  4       222              44  4       222              44  4       222\n  44444444  2222               44444444  2222               44444444  2222\n     444   2222222                444   2222222                444   2222222")
    st.write("#")

    def second42chart():
        st.text("Dans ce 3Dscatter plot nous avons la valeur fonciere d'un bien en fonction de sa longitude et latitude:")

        fig = px.scatter_3d(df.head(42), x='valeur_fonciere2020', y='longitude', z='latitude')
        
        st.plotly_chart(fig)

    second42chart()

    st.text("°     44    2222                   44    2222                   44    2222\n     444   222222                 444   222222                 444   222222\n   44  4       222              44  4       222              44  4       222\n  44444444  2222               44444444  2222               44444444  2222\n     444   2222222                444   2222222                444   2222222")
    st.write("#")

    def trosieme42chart():
        st.text("Dans ce 3Dscatter plot nous avons la surface terrain d'un bien en fonction de sa longitude et latitude:")
        fig = px.scatter_3d(df.head(42), x='surface_terrain', y='longitude', z='latitude')
        
        st.plotly_chart(fig)
    
    trosieme42chart()
    
    st.text("°     44    2222                   44    2222                   44    2222\n     444   222222                 444   222222                 444   222222\n   44  4       222              44  4       222              44  4       222\n  44444444  2222               44444444  2222               44444444  2222\n     444   2222222                444   2222222                444   2222222")
    st.write("#")

    def quatrieme42chart():
        st.text("Dans ce 3Dscatter plot nous avons le nom commune d'un bien en fonction de sa longitude et latitude: :")
        fig = px.scatter_3d(df.head(42), x='nom_commune', y='longitude', z='latitude')
        
        st.plotly_chart(fig)
    
    quatrieme42chart()

    st.text("°  ___  _____              ___  _____              ___  _____              ___  _____\n  /   |/ __  \            /   |/ __  \            /   |/ __  \            /   |/ __  \ \n / /| |`' / /'           / /| |`' / /'           / /| |`' / /'           / /| |`' / /'\n/ /_| |  / /            / /_| |  / /            / /_| |  / /            / /_| |  / /\n\___  |./ /___          \___  |./ /___          \___  |./ /___          \___  |./ /___\n    |_/\_____/              |_/\_____/              |_/\_____/              |_/\_____/")
        
        
if option == 'Numéro 42':
    numero42()

#########################################################




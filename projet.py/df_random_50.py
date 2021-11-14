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

dfold =  pd.read_csv("full_2020_25.csv")

req_col=['date_mutation','nature_mutation','valeur_fonciere','code_postal','nom_commune','type_local','surface_reelle_bati','nombre_pieces_principales','nature_culture','surface_terrain','longitude','latitude']
dfold = pd.read_csv("full_2020_25.csv",usecols=req_col,parse_dates=['date_mutation'],dtype={("nature_mutation ","nom_commune","nature_culture"):"category",("valeur_fonciere","surface_relle_bati","nombre_pieces_principales","surface_terrain","longitude","latitude","code_postal") : "float32"})
dfold['date_mutation']=pd.to_datetime(dfold["date_mutation"])  
dfold = dfold.sample(frac=0.25)
#la commande en dessous à été mis en commentaire car cela permet ainsi de pouvoir gardé les mêmes données aléatoires dans un nouveau csv et de ne par 
#avoir un nouveau csv chargé avec des nouvelles données à chaque fois
dfold.to_csv('full_2020_17.csv')

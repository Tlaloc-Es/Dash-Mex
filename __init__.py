import dash
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import json


FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, FA])
app.config.suppress_callback_exceptions = True
server = app.server

with open('./data/geo/estados.geojson') as f:
    STATES = json.load(f)

VPC = pd.read_csv('./data/economia/u_vulnerable_por_carencias.csv')
VPI = pd.read_csv('./data/economia/u_vulnerable_por_ingresos.csv')

SSA = pd.read_csv('./data/economia/u_ancianos_sin_ss.csv')
SSO = pd.read_csv('./data/economia/u_ocupada_sin_ss.csv')
SSN = pd.read_csv('./data/economia/u_no_ocupada_sin_ss.csv')

PT = pd.read_csv('./data/economia/u_pisos_tierra.csv')
PE = pd.read_csv('./data/economia/u_techo_endeble.csv')
PH = pd.read_csv('./data/economia/u_hacinados.csv')

LIBERTAD = pd.read_csv('./data/economia/u_libertad_economica.csv')
LIBERTAD_MEXICO = pd.read_csv('./data/economia/u_libertad_economica_mexico.csv')
PESOS = pd.read_csv('./data/economia/u_USD_MXN.csv')
LINEAS = pd.read_csv('./data/economia/u_lineas_pobreza_ingresos_1992_2019.csv')

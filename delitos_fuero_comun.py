#-*- coding: utf-8 -*-
# Esta es la página para delitos del fuero común

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import plotly.express as px
import plotly.figure_factory as ff

from dash.dependencies import Input, Output

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import pandas as pd

from chart_generator import generate_map
from chart_generator import generate_bars
from chart_generator import generate_maps
from chart_generator import generate_chart_top
from chart_generator import generate_comparative_bars
from chart_generator import generate_scatter
from chart_generator import generate_parcats_2
from chart_generator import generate_comparative_chart_top, generate_spline

from __init__ import *

# Se definen las variables de título y figuras, para poder actualizarlas directamente desde las funciones de los callback
title = 'Víctimas del Fuero Común, 2015 - 2019'

fig_a = 'delito-fuero-a'
fig_b = 'delito-fuero-b'
fig_c = 'delito-fuero-c'
fig_d = 'delito-fuero-d'
fig_e = 'delito-fuero-e'

# Se carga el dataset que se utiliza en esta página
DATA = pd.read_csv('./data/delitos/u_nueva_metodologia_fuero_comun.csv')
YEARS = DATA['Año'].unique()

# Dado que los delitos estan dividos en varias subcategorias, se elige la categoría que serviraá de filtro principal en las consultas
MAIN_FILTER = 'Tipo de delito'
TIPOS_DELITO = DATA[MAIN_FILTER].unique()

# Se genera el menú de variables para hacer las consultas en esta página
submenu = [
    html.Br(),
    html.H1("Configuración", className="lead"),
    
    dbc.FormGroup([
        dbc.Label(MAIN_FILTER),
        dcc.Dropdown(
            id="in-delito",
            value=TIPOS_DELITO[0],
            options=[
                {"label": col, "value": col} for col in DATA[MAIN_FILTER].unique()
            ]
        ),


        dbc.Label("Año de ocurrencia"),
        dcc.Dropdown(
            id="in-year",
            value=YEARS[0],
            options=[
                {"label": str(YEARS[i]), "value": YEARS[i]} for i in range(len(YEARS))
            ]
        )
    ]),

    dbc.RadioItems(
        id="in-options",
        options=[
            {"label": "No separar", "value": None},
            {"label": "Separar en años", "value": 'Años'},
            {"label": "Separar por sexo", "value": 'Sexo'},
            {"label": "Separar por edad", "value": 'Edad'}
        ],
        value=None,
    )
]

# Se genera el layout para imprimir los gráficos
layout = html.Div([

    html.Div([
        html.Div([
            html.Div([html.H1(title)], className="col"),
        ], className="row"),

        html.Div([
            html.Div([dcc.Graph(id=fig_a)], className="col"),
        ], className="row"),

        html.Div([
            html.Div([dcc.Graph(id=fig_b)], className="col"),
            html.Div([dcc.Graph(id=fig_c)], className="col"),
        ], className="row"),
        
        html.Div([
            html.Div([dcc.Graph(id=fig_d)], className="col"),
            html.Div([dcc.Graph(id=fig_e)], className="col"),
        ], className="row"),
    ], className="container")

])

# El callback, esta es la función que generará el gráfico dependiendo de las variable elegidas en el submenu
@app.callback(
    [Output(fig_a, 'figure'),
    Output(fig_b, 'figure'),
    Output(fig_c, 'figure'),
    Output(fig_d, 'figure'),
    Output(fig_e, 'figure')],
    [Input('in-delito', 'value'),
    Input('in-year', 'value'),
    Input('in-options', 'value')]
)
def update_delito(delito, year, options):
    
    # Se acceden a las variables globales con el dataset
    global MAIN_FILTER
    global STATES
    global YEARS
    global DATA

    # Se copia el dataset en una variable nueva, y se hace la consulta necesaria
    df = DATA.copy()
    df = df[df[MAIN_FILTER]==delito]
    df = df.groupby('Año').sum()
    df = df.reset_index()

    fig_d = px.scatter(df, x='Año', y='Total')

    # Dependiendo de las opciones de visualición seleccionadas se hara uno de los siguientes procesados
    if options == 'Años':
        fig_a = generate_maps(DATA, MAIN_FILTER, delito, 'Total', 'Entidad', STATES, 'properties.NOMGEO', f'Evolución de los casos de {delito} desde {YEARS[0]} hasta {YEARS[-1]}')
        fig_b = generate_spline(DATA, MAIN_FILTER, delito, 'Total', f'Evolucion del numero de {delito} desde {YEARS[0]} hasta {YEARS[-1]}')
        fig_c = generate_scatter(DATA, year, MAIN_FILTER, delito, 'Año', 'Rango de edad', 'Veces que ocurrio el delito', 'Años', f'Nº de veces que ocurrio {delito} desde {YEARS[0]} hasta {YEARS[-1]} por rango de edad')
        fig_d = generate_scatter(DATA, year, MAIN_FILTER, delito, 'Año', 'Sexo', 'Veces que ocurrio el delito', 'Años', f'Nº de veces que ocurrio {delito} desde {YEARS[0]} hasta {YEARS[-1]} por sexo')
        group = ['Año', 'Entidad', 'Sexo']
        fig_e = generate_parcats_2(DATA, group, filter=MAIN_FILTER, filter_value=delito, title=f'Nº de {delito} por sexo desde {YEARS[0]} hasta {YEARS[-1]}')
    elif options == 'Sexo':
        fig_a = generate_map(DATA, MAIN_FILTER, delito, 'Entidad', year, STATES, 'properties.NOMGEO', 'Total', f'Total {delito} en {year}')
        fig_b = generate_comparative_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde mas ocurrio {delito} en {year} a: ', 'Sexo', ['Mujer', 'Hombre'], True)
        fig_c = generate_comparative_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde menos ocurrio {delito} en {year} a: ', 'Sexo', ['Mujer', 'Hombre'], False)
        fig_d = generate_scatter(DATA, year, MAIN_FILTER, delito, 'Entidad', 'Sexo', 'Veces que ocurrio el delito', 'Estados', f'Nº de veces que ocurrio {delito} en {year} por sexo')
        group = ['Año', 'Entidad','Sexo']
        fig_e = generate_parcats_2(DATA, group, filter=MAIN_FILTER, filter_value=delito, year=year, title=f'Nº de {delito} por sexo en {year} en cada cada estado')
    elif options == 'Edad':
        fig_a = generate_maps(DATA, MAIN_FILTER, delito, 'Total', 'Entidad', STATES, 'properties.NOMGEO', f'Evolución de los casos de {delito} desde {YEARS[0]} hasta {YEARS[-1]}')
        fig_a = generate_map(DATA, MAIN_FILTER, delito, 'Entidad', year, STATES, 'properties.NOMGEO', 'Total', f'Total {delito} en {year}')
        fig_b = generate_comparative_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde mas ocurrio {delito} en {year} a: ', 'Rango de edad', ['Menor', 'Adulto'], True)
        fig_c = generate_comparative_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde menos ocurrio {delito} en {year} a: ', 'Rango de edad', ['Menor', 'Adulto'], False)
        fig_d = generate_scatter(DATA, year, MAIN_FILTER, delito, 'Entidad', 'Rango de edad', 'Año', 'Rango de edad', f'Nº de veces que ocurrio {delito} en {year} por rango de edad')
        group = ['Año', 'Entidad','Rango de edad']
        fig_e = generate_parcats_2(DATA, group, filter=MAIN_FILTER, filter_value=delito, year=year, title=f'Nº de {delito} por rango de edad desde {YEARS[0]} hasta {YEARS[-1]} en cada estado')
    else:
        fig_a = generate_map(DATA, MAIN_FILTER, delito, 'Entidad', year, STATES, 'properties.NOMGEO', 'Total', f'Total {delito} en {year}')
        fig_c = generate_comparative_bars(DATA, MAIN_FILTER, delito, year, f'{delito} frente al resto de delitos')
        fig_b = generate_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde mas ocurre el delito de {delito}')
        fig_d = generate_scatter(DATA, year, MAIN_FILTER, delito, 'Entidad', 'Rango de edad', 'Veces que ocurrio el delito', 'Estados', f'{delito} dividido por sexo y estados en {year}')
        group = ['Año', 'Entidad','Sexo']
        fig_e = generate_parcats_2(DATA, group, filter=MAIN_FILTER, filter_value=delito, year=year, title=f'Nº de {delito} por sexo en {year} en cada cada estado')

    # Se retornan los graficos generados
    return [fig_a, fig_b, fig_c, fig_d, fig_e]

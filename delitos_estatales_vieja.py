#-*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import plotly.express as px

from dash.dependencies import Input, Output

import pandas as pd

from chart_generator import generate_map, generate_bars, generate_maps
from chart_generator import generate_chart_top, generate_comparative_bars, generate_spline
from chart_generator import cor_indicator, generate_box, generate_box_all
from chart_generator import generate_spline_ile

from __init__ import *


title = 'Cifras de Incidencia Delictiva Estatal, 1997 - 2017'

fig_a = 'delito-vieja-estatal-a'
fig_b = 'delito-vieja-estatal-b'
fig_c = 'delito-vieja-estatal-c'
fig_d = 'delito-vieja-estatal-d'
fig_e = 'delito-vieja-estatal-e'

DATA = pd.read_csv('./data/delitos/u_vieja_metodologia_delictiva_estatal.csv')
YEARS = DATA['Año'].unique()
MAIN_FILTER = 'Modalidad'
TIPOS_DELITO = DATA[MAIN_FILTER].unique()

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


    dbc.Checklist(
        options=[{"label": "Separar en años", "value": True}],
        value=[],
        id="in-all-maps",
        switch=True,
    ),
]


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


@app.callback(
    [Output(fig_a, 'figure'),
    Output(fig_b, 'figure'),
    Output(fig_c, 'figure'),
    Output(fig_d, 'figure'),
    Output(fig_e, 'figure'),],
    [Input('in-delito', 'value'),
    Input('in-year', 'value'),
    Input('in-all-maps', 'value')]
)
def update_delito(delito, year, all):
    
    global MAIN_FILTER
    global STATES
    global YEARS
    global DATA

    df = DATA.copy()
    df = df[df[MAIN_FILTER] == delito]
    df = df.groupby('Año').sum()
    df = df.reset_index()

    if len(all) == 1:
        fig_a = generate_maps(DATA, MAIN_FILTER, delito, 'Total', 'Entidad', STATES, 'properties.NOMGEO', f'Evolución de los casos de {delito} desde {YEARS[0]} hasta {YEARS[-1]}')
        fig_b = generate_bars(DATA, MAIN_FILTER, delito, 'Total', f'{delito} frente al resto')
        fig_c = generate_spline(DATA, MAIN_FILTER, delito, 'Total', f'Evolucion del numero de {delito} desde {YEARS[0]} hasta {YEARS[-1]}')
        fig_d = generate_box_all(DATA, MAIN_FILTER, delito)
        fig_e = generate_spline_ile(DATA, MAIN_FILTER, delito, f'Relacion entre el delito y la libertad economica')
    else:
        fig_a = generate_map(DATA, MAIN_FILTER, delito, 'Entidad', year, STATES, 'properties.NOMGEO', 'Total', f'Total {delito} en {year}')
        fig_b = generate_comparative_bars(DATA, MAIN_FILTER, delito, year, f'{delito} frente al resto de delitos')
        fig_c = generate_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde mas ocurre el delito de {delito}')
        fig_d = cor_indicator(DATA, MAIN_FILTER, delito, year, f'Correlacion entre libertad economica y el delito {delito} en el año {year}')
        fig_e = generate_box(DATA, MAIN_FILTER, delito, year)
        if fig_d == {}:
            fig_d = generate_chart_top(DATA, MAIN_FILTER, delito, year, f'Los 5 estados donde mas ocurre el delito de {delito}', order=False)

    return [fig_a, fig_b, fig_c, fig_d, fig_e]

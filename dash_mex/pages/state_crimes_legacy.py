import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

from dash_mex.app_state import STATES, app
from dash_mex.charts import (
    cor_indicator,
    generate_bars,
    generate_box,
    generate_box_all,
    generate_chart_top,
    generate_comparative_bars,
    generate_map,
    generate_maps,
    generate_spline,
    generate_spline_ile,
)

title = 'Incidencia delictiva estatal (metodología previa, 1997-2017)'

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
    html.H1('Filtros', className='lead'),
    html.Div(
        [
            dbc.Label(MAIN_FILTER),
            dcc.Dropdown(
                id='in-delito',
                value=TIPOS_DELITO[0],
                options=[{'label': col, 'value': col} for col in DATA[MAIN_FILTER].unique()],
            ),
            dbc.Label('Año'),
            dcc.Dropdown(
                id='in-year',
                value=YEARS[0],
                options=[{'label': str(YEARS[i]), 'value': YEARS[i]} for i in range(len(YEARS))],
            ),
        ],
        className='mb-3',
    ),
    dbc.Checklist(
        options=[{'label': 'Mostrar serie temporal por año', 'value': True}],
        value=[],
        id='in-all-maps',
        switch=True,
    ),
]


layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div([html.H1(title)], className='col'),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=fig_a), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=fig_b), type='circle')], className='col'
                        ),
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=fig_c), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=fig_d), type='circle')], className='col'
                        ),
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=fig_e), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
            ],
            className='container',
        )
    ]
)


@app.callback(
    [
        Output(fig_a, 'figure'),
        Output(fig_b, 'figure'),
        Output(fig_c, 'figure'),
        Output(fig_d, 'figure'),
        Output(fig_e, 'figure'),
    ],
    [Input('in-delito', 'value'), Input('in-year', 'value'), Input('in-all-maps', 'value')],
)
def update_delito(delito, year, all):

    global MAIN_FILTER
    global STATES
    global YEARS
    global DATA

    filtered_data = DATA[DATA[MAIN_FILTER] == delito].copy()

    if len(all) == 1:
        fig_a = generate_maps(
            filtered_data,
            MAIN_FILTER,
            delito,
            'Total',
            'Entidad',
            STATES,
            'properties.NOMGEO',
            f'Evolución de los casos de {delito} desde {YEARS[0]} hasta {YEARS[-1]}',
        )
        fig_b = generate_bars(
            filtered_data, MAIN_FILTER, delito, 'Total', f'{delito} frente al resto'
        )
        fig_c = generate_spline(
            filtered_data,
            MAIN_FILTER,
            delito,
            'Total',
            f'Evolucion del numero de {delito} desde {YEARS[0]} hasta {YEARS[-1]}',
        )
        fig_d = generate_box_all(filtered_data, MAIN_FILTER, delito)
        fig_e = generate_spline_ile(
            filtered_data, MAIN_FILTER, delito, 'Relacion entre el delito y la libertad economica'
        )
    else:
        fig_a = generate_map(
            filtered_data,
            MAIN_FILTER,
            delito,
            'Entidad',
            year,
            STATES,
            'properties.NOMGEO',
            'Total',
            f'Total {delito} en {year}',
        )
        fig_b = generate_comparative_bars(
            DATA, MAIN_FILTER, delito, year, f'{delito} frente al resto de delitos'
        )
        fig_c = generate_chart_top(
            filtered_data,
            MAIN_FILTER,
            delito,
            year,
            f'Los 5 estados donde mas ocurre el delito de {delito}',
        )
        fig_d = cor_indicator(
            filtered_data,
            MAIN_FILTER,
            delito,
            year,
            f'Correlacion entre libertad economica y el delito {delito} en el año {year}',
        )
        fig_e = generate_box(filtered_data, MAIN_FILTER, delito, year)
        if fig_d == {}:
            fig_d = generate_chart_top(
                filtered_data,
                MAIN_FILTER,
                delito,
                year,
                f'Los 5 estados donde mas ocurre el delito de {delito}',
                order=False,
            )

    return [fig_a, fig_b, fig_c, fig_d, fig_e]

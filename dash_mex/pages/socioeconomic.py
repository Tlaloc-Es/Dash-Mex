# Esta es la página para las variables socioecnómicas
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

from dash_mex.app_state import STATES, app, get_socioeconomic_data
from dash_mex.charts import make_title


def _build_social_indicators():
    datasets = get_socioeconomic_data()
    return [
        ['porcentaje de la poblacion vulnerable por carencias sociales', datasets['VPC'], False],
        ['porcentaje de la poblacion vulnerable por ingresos', datasets['VPI'], False],
        [
            'porcentaje de la poblacion no economicamente activa sin acceso a la seguridad social',
            datasets['SSN'],
            False,
        ],
        [
            'porcentaje de la poblacion de 65 años o mas sin acceso a la seguridad social',
            datasets['SSA'],
            False,
        ],
        [
            'porcentaje de la poblacion ocupada sin acceso a la seguridad social',
            datasets['SSO'],
            False,
        ],
        ['porcentaje de la poblacion en viviendas con hacinamiento', datasets['PH'], False],
        [
            'porcentaje de la poblacion en viviendas con techos de material endeble',
            datasets['PE'],
            False,
        ],
        ['porcentaje de la poblacion en viviendas con pisos de tierra', datasets['PT'], False],
    ]


# Se definen las variables de título y figuras, para poder actualizarlas directamente desde las funciones de los callback
TITLE = 'Análisis socioeconómico por entidad'

FIG_A = 'socioeconomico-a'
FIG_B = 'socioeconomico-b'
FIG_C = 'socioeconomico-c'
FIG_D = 'socioeconomico-d'
FIG_E = 'socioeconomico-e'

# Se generan las opciones para la visualización.
INDICADORES_SOCIALES = _build_social_indicators()

YEARS = list(range(2008, 2019, 2))

# Se genera el menú de variables para hacer las consultas en esta página
submenu = [
    html.Br(),
    html.H1('Filtros', className='lead'),
    html.Div(
        [
            dbc.Label('Indicador socioeconómico'),
            dcc.Dropdown(
                id='in-social',
                value=0,
                options=[
                    {'label': INDICADORES_SOCIALES[i][0], 'value': i}
                    for i in range(len(INDICADORES_SOCIALES))
                ],
            ),
        ],
        className='mb-3',
    ),
]

# Se genera el layout para imprimir los gráficos
layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div([html.H1(TITLE)], className='col'),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=FIG_A), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=FIG_B), type='circle')], className='col'
                        ),
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=FIG_C), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=FIG_D), type='circle')], className='col'
                        ),
                        html.Div(
                            [dcc.Loading(dcc.Graph(id=FIG_E), type='circle')], className='col'
                        ),
                    ],
                    className='row',
                ),
            ],
            className='container',
        )
    ]
)


def difference(df):
    a = df.loc[df['Año'] == 2008, 'Porcentage']
    b = df.loc[df['Año'] == 2018, 'Porcentage']

    if a.empty or b.empty:
        return 0.0

    return round(float(a.mean() - b.mean()), 2)


# El callback, esta es la función que generará el gráfico dependiendo de las variable elegidas en el submenu
@app.callback(
    [
        Output(FIG_A, 'figure'),
        Output(FIG_B, 'figure'),
        Output(FIG_C, 'figure'),
        Output(FIG_D, 'figure'),
        Output(FIG_E, 'figure'),
    ],
    [Input('in-social', 'value')],
)
def update_social(indicador):

    # Se acceden a las variables globales con el dataset
    global STATES

    data = INDICADORES_SOCIALES[int(indicador)][1]
    inverso = INDICADORES_SOCIALES[int(indicador)][2]

    # Se copia el dataset en una variable nueva, y se hace la consulta necesaria
    delta = data.pivot_table(index='Entidad', columns='Año', values='Porcentage', aggfunc='mean')
    df = delta.reset_index()
    df['Porcentage'] = (df.get(2008, 0).fillna(0) - df.get(2018, 0).fillna(0)).round(2)
    keep_columns = ['Entidad', 'Porcentage']
    df = df[keep_columns]

    peores = df.sort_values('Porcentage')[:5]['Entidad'].values
    mejores = df.sort_values('Porcentage')[-5:]['Entidad'].values

    # Dado que algunos datos de caracter lineal son mejores cuando la pendiente desciende y otros cuando la pendiente asciende, de esta manera le damos la vuelta a esos datos, para que la pendiende indique siempre lo mismo con la otra variable con la que se va a comparar
    if inverso:
        fig_b = get_scatter(data.copy(), mejores, 'Estados que peor evolucionan')
        fig_c = get_scatter(data.copy(), peores, 'Estados que mejor evolucionan')
    else:
        fig_b = get_scatter(data.copy(), peores, 'Estados que peor evolucionan')
        fig_c = get_scatter(data.copy(), mejores, 'Estados que mejor evolucionan')

    fig_d = comparacion()
    fig_e = comparacion(desagregacion=False)

    fig_a = get_mapas(data.copy(), INDICADORES_SOCIALES[int(indicador)][0])

    return [fig_a, fig_b, fig_c, fig_d, fig_e]


def get_scatter(data, filter, title):
    # Esta funcion sirve para generar un scatter plot con mas de una variable
    years = data['Año'].unique()

    data.copy()

    fig_line = go.Figure(data=go.Scatter())

    fig_line = go.Figure()
    for i in filter:
        fig_line.add_trace(
            go.Scatter(
                x=years, y=data[data['Entidad'] == i]['Porcentage'], mode='lines+markers', name=i
            )
        )

    mean_by_year = data.groupby('Año')['Porcentage'].mean()
    fig_line.add_trace(go.Scatter(x=years, y=mean_by_year, mode='lines+markers', name='Media'))

    fig_line.update_layout(
        title=title,
    )

    return fig_line


def comparacion(desagregacion=True):
    # Esta función es para generar un scatter plot, con los datos del precio de la canasta, el precio del dolar, y el indice de libertad economica

    datasets = get_socioeconomic_data()
    libertad_mexico = datasets['LIBERTAD_MEXICO'].copy()
    pesos = datasets['PESOS'].copy()
    lineas = datasets['LINEAS'].copy()

    df = pd.merge(pesos, lineas, how='right', on=['Fecha'])

    df['lpei'] = df['lpei'] / df['lpei'].max()
    df['lpi'] = df['lpi'] / df['lpi'].max()
    df['Price'] = df['Price'] / df['Price'].max()
    libertad_mexico['ile'] = libertad_mexico['ile'] / libertad_mexico['ile'].max()

    if desagregacion:
        df = df[df['desagregacion'] == 'Rural']
        fig = go.Figure(layout=make_title('Comparación porcentual, en desagregacion rural'))
    else:
        df = df[df['desagregacion'] == 'Urbano']
        fig = go.Figure(layout=make_title('Comparación porcentual, en desagregacion urbana'))

    fig.add_trace(
        go.Scatter(
            x=df['Fecha'],
            y=df['lpei'],
            name='Línea de pobreza extrema por ingresos',
            line_shape='spline',
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df['Fecha'], y=df['lpi'], name='Línea de pobreza por ingresos', line_shape='spline'
        )
    )

    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Price'], name='USD - MXN', line_shape='spline'))

    fig.add_trace(
        go.Scatter(
            x=libertad_mexico['Año'],
            y=libertad_mexico['ile'],
            name='Indice de libertad economica',
            line_shape='spline',
        )
    )

    return fig


def get_mapas(info, title):
    # Sirve para generar los mapas, dado que se quiere visualizar mas de un mapa a la vez, el proceso es iterativo

    df = info.copy()
    years = df['Año'].unique()

    data = []
    layout = dict(
        title=title.title(),
        showlegend=True,
        autosize=True,
    )

    porcentage_max = 0

    for i in range(len(years)):
        geo_key = 'geo' + str(i + 1) if i != 0 else 'geo'

        df = info.copy()
        df = df[df['Año'] == years[i]]
        df = df.groupby('Entidad').sum()
        df = df.reset_index()

        if df['Porcentage'].max() > porcentage_max:
            df['Porcentage'].max()

        data.append(
            dict(
                z=df['Porcentage'],
                type='choropleth',
                geojson=STATES,
                locations=df['Entidad'],
                featureidkey='properties.NOMGEO',
                geo=geo_key,
                text=[years[i]],
                name=str(years[i]),
                zmin=0,
                zmax=100,
                colorscale='Reds',
                # colorbar_title = porcentage_max
            )
        )

        data.append(
            dict(
                type='scattergeo',
                showlegend=False,
                lon=[-94.52],
                lat=[30.71],
                geo=geo_key,
                text=[years[i]],
                mode='text',
            )
        )

        layout[geo_key] = dict(
            landcolor='rgb(229, 229, 229)',
            visible=False,
            fitbounds='locations',
            domain=dict(x=[], y=[]),
            subunitcolor='rgb(255, 255, 255)',
        )

    z = 0
    COLS = 3
    ROWS = 2
    for y in reversed(range(ROWS)):
        for x in range(COLS):
            geo_key = 'geo' + str(z + 1) if z != 0 else 'geo'
            layout[geo_key]['domain']['x'] = [float(x) / float(COLS), float(x + 1) / float(COLS)]
            layout[geo_key]['domain']['y'] = [float(y) / float(ROWS), float(y + 1) / float(ROWS)]
            z = z + 1
            if z > len(years) - 1:
                break

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(width=1000)
    return fig

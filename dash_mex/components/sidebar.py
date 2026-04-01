import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

from dash_mex.app_state import app

# Estas funciones son solo para establecer el sidebar del dashboard con su estilo y los menus

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
    'background-color': '#f8f9fa',
}


submenu_1 = [
    html.Li(
        dbc.Row(dbc.NavLink('Inicio', href='/')),
    ),
    html.Li(
        dbc.Row(
            [
                dbc.Col('Delitos'),
                dbc.Col(html.I(className='fas fa-chevron-right mr-3'), width='auto'),
            ],
            className='my-1',
        ),
        id='submenu-1',
    ),
    dbc.Collapse(
        [
            dbc.NavLink(
                'Incidencia estatal (metodología previa, 1997-2017)',
                href='/delitos-estatales-vieja',
            ),
            dbc.NavLink('Víctimas del fuero común (2015-2019)', href='/fuero-comun'),
            dbc.NavLink('Incidencia federal (2012-2019)', href='/delitos-federales'),
        ],
        id='submenu-1-collapse',
    ),
]


submenu_2 = [dbc.NavLink('Contexto socioeconómico', href='/socioeconomico')]

sidebar = html.Div(
    [
        html.H1('Panel de navegación', className='lead'),
        dbc.Nav(submenu_1 + submenu_2, vertical=True),
        html.Hr(),
        dbc.Nav(id='custom-nav', vertical=True),
    ],
    style=SIDEBAR_STYLE,
    id='sidebar',
)


# this function is used to toggle the is_open property of each Collapse
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return 'open'
    return ''


for i in [1, 2]:
    app.callback(
        Output(f'submenu-{i}-collapse', 'is_open'),
        [Input(f'submenu-{i}', 'n_clicks')],
        [State(f'submenu-{i}-collapse', 'is_open')],
    )(toggle_collapse)

    app.callback(
        Output(f'submenu-{i}', 'className'),
        [Input(f'submenu-{i}-collapse', 'is_open')],
    )(set_navitem_class)

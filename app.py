#-*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from __init__ import *

from index import index_page

from delitos_estatales_vieja import layout as vde
from delitos_estatales_vieja import submenu as sub_vde

from delitos_fuero_comun import layout as dfc
from delitos_fuero_comun import submenu as sub_dfc

from delitos_federales import layout as df
from delitos_federales import submenu as sub_df

from socioeconomico import layout as layout_social
from socioeconomico import submenu as sub_social

from sidebar import sidebar

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


app.layout = html.Div([
    sidebar,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style=CONTENT_STYLE)
])

# Esta funcion sirve para hacer el routing de la aplicación
@app.callback(
    [Output('page-content', 'children'),
     Output('custom-nav', 'children')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/delitos-estatales-vieja':
        return [vde, sub_vde]
    elif pathname == '/fuero-comun':
        return [dfc, sub_dfc]
    elif pathname == '/delitos-federales':
        return [df, sub_df]
    elif pathname == '/socioeconomico':
        return [layout_social, sub_social]
    else:
        return [index_page, None]


if __name__ == "__main__":
    app.run_server(debug=True)

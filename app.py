from dash import dcc, html
from dash.dependencies import Input, Output

from dash_mex.app_state import app
from dash_mex.components.sidebar import sidebar
from dash_mex.pages.common_jurisdiction_crimes import layout as dfc
from dash_mex.pages.common_jurisdiction_crimes import submenu as sub_dfc
from dash_mex.pages.federal_crimes import layout as df
from dash_mex.pages.federal_crimes import submenu as sub_df
from dash_mex.pages.home import get_index_page
from dash_mex.pages.socioeconomic import layout as layout_social
from dash_mex.pages.socioeconomic import submenu as sub_social
from dash_mex.pages.state_crimes_legacy import layout as vde
from dash_mex.pages.state_crimes_legacy import submenu as sub_vde

CONTENT_STYLE = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}


app.layout = html.Div(
    [
        sidebar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


# Esta función sirve para hacer el routing de la aplicación
@app.callback(
    [Output('page-content', 'children'), Output('custom-nav', 'children')],
    [Input('url', 'pathname')],
)
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
        return [get_index_page(), None]


if __name__ == '__main__':
    app.run_server(debug=True)

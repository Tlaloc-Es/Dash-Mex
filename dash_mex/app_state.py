import json
from functools import lru_cache
from pathlib import Path

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash

FA = 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX, FA],
    assets_folder=str(PROJECT_ROOT / 'assets'),
)
app.config.suppress_callback_exceptions = True
server = app.server

with open(DATA_DIR / 'geo' / 'estados.geojson', encoding='utf-8') as f:
    STATES = json.load(f)


@lru_cache(maxsize=1)
def get_socioeconomic_data():
    """Lazy-load socioeconomic datasets to reduce app startup time."""
    data_dir = DATA_DIR / 'economia'
    return {
        'VPC': pd.read_csv(data_dir / 'u_vulnerable_por_carencias.csv'),
        'VPI': pd.read_csv(data_dir / 'u_vulnerable_por_ingresos.csv'),
        'SSA': pd.read_csv(data_dir / 'u_ancianos_sin_ss.csv'),
        'SSO': pd.read_csv(data_dir / 'u_ocupada_sin_ss.csv'),
        'SSN': pd.read_csv(data_dir / 'u_no_ocupada_sin_ss.csv'),
        'PT': pd.read_csv(data_dir / 'u_pisos_tierra.csv'),
        'PE': pd.read_csv(data_dir / 'u_techo_endeble.csv'),
        'PH': pd.read_csv(data_dir / 'u_hacinados.csv'),
        'LIBERTAD': pd.read_csv(data_dir / 'u_libertad_economica.csv'),
        'LIBERTAD_MEXICO': pd.read_csv(data_dir / 'u_libertad_economica_mexico.csv'),
        'PESOS': pd.read_csv(data_dir / 'u_USD_MXN.csv'),
        'LINEAS': pd.read_csv(data_dir / 'u_lineas_pobreza_ingresos_1992_2019.csv'),
    }

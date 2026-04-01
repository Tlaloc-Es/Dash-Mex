# Dash-Mex

Interactive dashboard on crime and socioeconomic context in Mexico, built with Dash and Plotly using official sources.

## What it offers

- Analysis of state crimes with historical methodology.
- Analysis of federal and common jurisdiction crimes with interactive filters.
- Socioeconomic views to compare trends between entities.
- Geospatial maps, comparisons by entity, and multidimensional visualizations.

## Visual Demo

You can add screenshots in assets and link them here to improve the repository presentation:

- assets/screenshot-home.png
- assets/screenshot-delitos.png
- assets/screenshot-socioeconomico.png

## Tech Stack

- Python 3.11+
- Dash 2.x
- Plotly 5.x
- Pandas 2.x
- GeoPandas
- Gunicorn
- uv for modern dependency management

## Installation

### Recommended option: uv

```bash
uv sync
```

## Local Usage

```bash
python3 app.py
```

Then open http://localhost:8050

**Note:** The app may take some time to load initially due to data processing.

## Production Execution

```bash
gunicorn app:server --bind 0.0.0.0:${PORT:-8000} --timeout 90
```

## Docker

```bash
docker build -t dash-mex .
docker run --rm -p 8000:8000 dash-mex
```

## Current Structure

```text
.
|-- app.py
|-- index.py
|-- dash_mex/
|   |-- __init__.py
|   |-- app_state.py
|   |-- charts.py
|   |-- components/
|   |   |-- __init__.py
|   |   `-- sidebar.py
|   `-- pages/
|       |-- __init__.py
|       |-- home.py
|       |-- federal_crimes.py
|       |-- common_jurisdiction_crimes.py
|       |-- state_crimes_legacy.py
|       `-- socioeconomic.py
|-- data/
|   |-- delitos/
|   |-- economia/
|   `-- geo/
|-- assets/
|-- pyproject.toml
|-- Dockerfile
|-- .pre-commit-config.yaml
|-- ruff.toml
`-- .codespellrc
```

## Data Sources

- SESNSP: open crime incidence.
- INEGI: geospatial resources.
- CONEVAL and complementary economic sources.

For the full data update plan, check [README_DATA_UPDATE.md](README_DATA_UPDATE.md).

## Contribution

1. Create a branch from master.
1. Implement small, focused changes.
1. Validate that the app starts and main routes work.
1. Open a Pull Request with context, changes, and visual evidence if applicable.

## Modernization Roadmap

- Complete migration to modular structure by layers.
- Caching of callbacks and load time optimization.
- Unit and integration test coverage.
- Automation of data update cycle.

## ⚠️ Dataset Coverage

The current version includes data up to 2019.

Future updates will incorporate more recent datasets and expanded indicators.

## Licencia

MIT

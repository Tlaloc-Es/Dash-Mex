#-*- coding: utf-8 -*-

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

import math


def make_title(title):
    return dict(
        title = title,
        autosize = True,
    )


def generate_parallel_categories(dataset, group, filter=None, filter_value=None, year=None):
    df = dataset.copy()

    group = ['Rango de edad', 'Sexo', 'Año', 'Total']
    year = 2015
    filter = 'Tipo de delito'
    filter_value = 'Homicidio'

    if filter_value != None:
        df = df[df[filter]==filter_value]

    if year != None:
        df = df[df['Año']==year]

    df = df.groupby(group).sum().reset_index()
    fig = px.parallel_categories(df, color="Total", color_continuous_scale='Bluered')

    fig.show()


def generate_parcats_2(dataset, group, filter=None, filter_value=None, year=None, title=None):
    df = dataset.copy()
    
    if filter_value != None:
        df = df[df[filter]==filter_value]

    if year != None:
        df = df[df['Año']==year]

    dimensions = []
    for i in group:
        dimensions.append(
            {'label': i,
            'values': df[i]}
        )

    fig = go.Figure(data = [go.Parcats(
        dimensions=dimensions,
        counts=df['Total']
    )], layout = make_title(title))

    return fig


def generate_parcats(dataset, dimensions, title):
    df = dataset.copy()
    df = df.sort_values(by=dimensions[0])
    dimensions_dict = []

    for i in dimensions_dict:
        dimensions.append(
            {'label': i,
            'values': list(df[i])}
        )

    fig = go.Figure(go.Parcats(dimensions=dimensions_dict))

    dimensions_parcast = []

    for i in dimensions:
        dimensions_parcast.append(go.parcats.Dimension(values=df[i], label=i))


    fig = go.Figure(data = [go.Parcats(
            dimensions=dimensions_parcast,
            hoveron='color', 
            hoverinfo='count+probability',
            labelfont={'size': 18, 'family': 'Times'},
            tickfont={'size': 16, 'family': 'Times'},
            arrangement='freeform')],
            layout = make_title(title))

    return fig


def generate_box(dataset, filter, filter_value, year):
    df = dataset.copy()

    df = df[(df['Año'] == year) & (df[filter] == filter_value)]
    df = df.groupby('Entidad').sum().reset_index()[['Entidad', 'Total']]

    fig = px.box(df, y="Total", points="all", hover_data=["Entidad"])

    return fig

def generate_box_all(dataset, filter, filter_value):
    df = dataset.copy()

    df = df[df[filter] == filter_value]
    df = df.groupby('Año').sum().reset_index()[['Año', 'Total']]

    fig = px.box(df, y="Total", points="all", hover_data=["Año"])

    return fig

def cor_indicator(df, filter, filter_value, year, title):
    dfl = pd.read_csv('./data/economia/u_libertad_economica.csv')
    result = pd.merge(df, dfl, how='right', on=['Entidad', 'Año'])

    if year in dfl['Año'].unique():
        result = result[(result['Año']==year) & (result[filter]==filter_value)].groupby(['Entidad', filter, 'ile'], as_index=False)['Total'].sum()

        result = result.drop(filter, axis=1).corr()['ile']['Total']

        if result >= 0:
            axis = {'range': [0, 1] }
            steps = [{'range': [0, 0.5], 'color': "blue"},
                    {'range': [0.5, 0.75], 'color': "purple"},
                    {'range': [0.75,  1], 'color': "red"}]
        elif result < 0:
            axis = {'range': [0, -1] }
            steps = [{'range': [0, -0.5], 'color': "blue"},
                    {'range': [-0.5, -0.75], 'color': "purple"},
                    {'range': [-0.75,  -1], 'color': "red"}]

        fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value=round(result, 2),
            mode = "gauge+number",
            title = {'text': title},
            gauge = {'axis': axis,
                    'steps' : steps,
                    'threshold' : {'line': {'color': "yellow", 'width': 4}, 'thickness': 1, 'value': result}}))

        return fig
    else:
        return {}


def generate_map(dataset, filter, filter_value, locations, year, geojson, featureidkey, color, title):
    
    df = dataset.copy()
    df = df[df[filter]==filter_value]
    df = df[df['Año'] == year]
    df = df.groupby(locations).sum()
    df = df.reset_index()

    fig = go.Figure(data=go.Choropleth(
        z = df[color],
        colorscale='Bluered',
        colorbar_title = "Total",
        geojson=geojson,
        locations=df[locations],
        featureidkey=featureidkey,
        text=f'Casos de {filter_value}'
    ),
    layout=make_title(title))          

    fig.update_geos(fitbounds="locations", visible=False)
        
    return fig


def generate_chart_top(dataset, filter, filter_value, year, title, other_filter=None, other_filter_value=None, chart=True, order=True):
    df = dataset.copy()

    if other_filter != None and other_filter_value != None:
        df = df[df[other_filter]==other_filter_value]

    df = df[(df['Año'] == year) & (df[filter] == filter_value)].groupby(['Entidad', filter]).sum().reset_index().drop([filter, 'Año'], axis=1).sort_values(['Total'], ascending=order).tail(5)

    bar = go.Bar(x=df['Total'], y=df['Entidad'], orientation='h')
    if chart:
        fig = go.Figure(bar, layout=make_title(title))
    else:
        fig = bar

    return fig


def generate_comparative_chart_top(dataset, filter, filter_value, year, title, other_filter, other_filter_values, order=True ):
    df = dataset.copy()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=other_filter_values
        )

    i = 1
    for value in other_filter_values:
        fig.add_trace(
            generate_chart_top(df, filter, filter_value, year, '', other_filter, value, chart=False, order=order),
            row=1, col=i
        )
        i += 1

    fig.update_layout(showlegend=False, title_text=title)

    return fig


def generate_scatter(dataset, year, filter, filter_value, x, y, x_label, y_label, title):
    df = dataset.copy()

    if x == 'Año':
        df = df[df[filter]==filter_value]
    else:
        df = df[(df['Año']==year) & (df[filter]==filter_value)]

    df.drop(df.columns.difference([x,y,'Total']), axis=1, inplace=True)
    df = df.groupby([x, y]).sum().reset_index()

    states = df[x].unique()

    fig = go.Figure()

    colores = ['green', 'blue', 'red', 'yellow', 'orange']

    i = 0
    for sexo in df[y].unique():
        fig.add_trace(go.Scatter(
            x=df[df[y] == sexo]['Total'],
            y=states,
            marker=dict(color=colores[i], size=12),
            mode="markers",
            name=sexo,
        ))
        i += 1

    fig.update_layout(title=title,
                    xaxis_title=x_label,
                    yaxis_title=y_label)

    return fig


def generate_pies(data, label, value):
        years = data['Año'].unique()

        traces = []
        z = 0
        COLS = 3
        ROWS = 2
        for y in range(ROWS):
            for x in range(COLS):
                df = data.copy()
                df = df[df['Año']==years[z]]
                df = df.groupby(label).sum()
                df=df.reset_index()

                domain = {
                        'x': [round(x/COLS, 2), round((x+1)/COLS, 2)], 
                        'y': [round(y/ROWS, 2), round((y+1)/ROWS, 2)]
                    }

                traces.append(
                    go.Pie(
                        labels = df[label],
                        values = df[value],
                        domain = domain,
                        showlegend = False,
                        hoverinfo = 'label+percent+name'
                        )
                )
                z=z+1
                if z > len(years)-1:
                    break
        
        layout = go.Layout(
                autosize = True,
                title = label
                )

        return go.Figure(data = traces, layout=make_title('Titulo'))


def generate_bars(dataset, filter, filter_value, value, title):
    df = dataset.copy()
    df = df[df[filter]==filter_value]
    df = df.groupby('Año').sum()
    df = df.reset_index()

    fig = px.bar(df, x='Año', y=value)   
    return fig


def generate_spline_ile(dataset, filter, filter_value, title):

    df = dataset.copy()

    dfl = pd.read_csv('./data/economia/u_libertad_economica.csv')
    dfl = dfl.groupby('Año').sum().reset_index()[['Año', 'ile']]
    dfl['ile'] = dfl['ile']/dfl['ile'].max()

    df = df[df[filter] == filter_value]
    df = df.groupby('Año').sum().reset_index()[['Año', 'Total']]

    df['Total'] = df['Total']/df['Total'].max()

    fig = go.Figure(layout=make_title(title))

    fig.add_trace(go.Scatter(
                        x=df['Año'], y=df['Total'], name="Total delito",
                        line_shape='spline'))

    fig.add_trace(go.Scatter(
                        x=dfl['Año'], y=dfl['ile'], name="Indice libertad economica",
                        line_shape='spline'))

    return fig


def generate_spline(dataset, filter, filter_value, value, title):
    df = dataset.copy()
    df = df[df[filter] == filter_value]
    df = df.groupby('Año').sum()
    df = df.reset_index()

    chart = go.Scatter(
        x=df['Año'], y=df[value], name="spline",
        line_shape='spline')

    return go.Figure(chart, layout=make_title(title))


def generate_comparative_bars(dataset, filter, filter_value, year, title):
    df = dataset.copy()
    df = df[df['Año']==year]
    df = df.groupby(filter).sum()
    df = df.reset_index()

    delitos = df[filter].unique()
    colors = ['lightslategray',] * len(delitos)

    colors[np.where(delitos == filter_value)[0][0]] = 'crimson'
    fig = go.Figure(data=[go.Bar(x=df[filter], y=df['Total'], marker_color=colors)], layout=make_title(title))
        
    return fig


def generate_maps(dataset, filter, filter_value, value, locations, geojson, featureidkey, title, split=True):
    
    df = dataset.copy()
    years = dataset['Año'].unique()

    data = []
    layout = dict(
        title = title,
        autosize = True,
    )

    total_max = 0

    if split:
        step = int(math.ceil(len(years)/6))

        years_a = []
        for i in range(0, len(years), step):
            years_a.append(years[i])

        years = years_a

    for i in range(len(years)):
        geo_key = 'geo'+str(i+1) if i != 0 else 'geo'

        df = dataset.copy()
        df = df[df[filter]==filter_value]
        df = df[df['Año']==years[i]]
        df = df.groupby(locations).sum()
        df = df.reset_index()


        data.append(
            dict(
                z=df[value],
                type = 'choropleth',
                geojson=geojson,
                locations=df[locations],
                featureidkey=featureidkey,
                geo = geo_key,
                text=f'Casos de {filter_value}',
                name = str(years[i])
            )
        )

        
        data.append(
            dict(
                type = 'scattergeo',
                showlegend = False,
                lon = [-94.52],
                lat = [30.71],
                geo = geo_key,
                text = [years[i]],
                mode = 'text',
            )
        )

        layout[geo_key] = dict(
            visible = False,
            fitbounds="locations",
            domain = dict( x = [], y = [] )
        )

        if df[value].max() > total_max:
            total_max = df[value].max()

    for i in range(len(data)):
        if data[i]['type'] == 'choropleth':
            data[i].update(zmin=0, zmax=total_max, colorscale='Bluered')

    z = 0
    COLS = 3
    ROWS = math.ceil(len(years)/COLS)
    for y in reversed(range(ROWS)):
        for x in range(COLS):
            geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
            layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
            layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
            z=z+1
            if z > len(years)-1:
                break

    fig = go.Figure(data=data, layout=layout)
    
    fig.update_layout(width=1000, coloraxis=dict(), legend_title_text='Trend')

    return fig

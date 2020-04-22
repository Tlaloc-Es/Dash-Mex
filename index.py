#-*- coding: utf-8 -*-

import pandas as pd
import dash_core_components as dcc
import dash_html_components as html

from chart_generator import generate_parcats

nmfc = pd.read_csv('./data/delitos/u_nueva_metodologia_fuero_comun.csv')
nmdf = pd.read_csv('./data/delitos/u_nueva_metodologia_delictiva_federal.csv')
vmdf = pd.read_csv('./data/delitos/u_vieja_metodologia_delictiva_estatal.csv')

dimensiones_a = ['Bien jurídico afectado', 'Tipo de delito', 'Subtipo de delito']
dimensiones_b = ['Ley', 'Concepto', 'Tipo']
dimensiones_c = ['Modalidad', 'Tipo', 'Subtipo']

fig_a = generate_parcats(nmfc, dimensiones_a, 'Disposicion de los delitos para nueva metodología del fuero común')
fig_b = generate_parcats(nmdf, dimensiones_b, 'Disposicion de los delitos para nueva metodología de incidencia delictiva federal')
fig_c = generate_parcats(vmdf, dimensiones_c, 'Disposicion de los delitos para vieja metodología de incidencia delictiva estatal')


index_page = html.Div([
    dcc.Markdown('''
        # Criminalidad
        Los datos de criminalidad se dividen en dos apartados nueva y vieja metodologia, ademas de que en cada apartado hay entre 3 y cuatro subapartados para recoger diferentes delitos

        **Nueva metodologia**
        * Cifras de Víctimas del Fuero Común, 2015 - 2019
        * Cifras de Incidencia Delictiva Federal, 2012 - 2019
        
        **Vieja metodologia**
        * Cifras de Incidencia Delictiva Estatal, 1997 - 2017

        **Fuentes de datos**
        * https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva

        **Enlaces de interes**
        * https://www.gob.mx/sesnsp/acciones-y-programas/incidencia-delictiva-87005?idiom=es
        * https://www.animalpolitico.com/2017/12/delictivo-nuevo-reporte-datos/
        * https://seguridad.nexos.com.mx/?p=1667
        * http://www.diputados.gob.mx/documentos/Congreso_Nacional_Legislativo/Doc/CMD_Integrado.pdf
        
        ## Criterio
        Todos los datos conseguidos por municipios son visualizados por estado, debido la gran cantidad de municipios que tiene mexico, y el procesado seria lento y requeriria un gran ancho de banda.

        Los delitos como se puede ver a continuación estan divididos en varias clases con sus propias subclases, de la siguiente manera:
        '''),
        
    dcc.Graph(figure = fig_a),
    dcc.Graph(figure = fig_b),
    dcc.Graph(figure = fig_c),

    dcc.Markdown('''
        # Geo
        Los datos para representar los estados han sido descargados desde la página de la INEGI
        * https://www.inegi.org.mx/app/mapas/

        # Socioeconomico
        Hay diferentes datasets para visualizar información socio economico, a continuación se colocaran los datos que se pueden sacar y el enlace:

        Porcentaje de la poblacion vulnerable por carencias sociales, 2008 - 2018
        * Dataset: Porcentaje, número de personas y carencias promedio por indicador de pobreza, según entidad federativa, 2008-2018, parte II
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/da89fadd-0f0e-425a-a7bb-154d091a51d7
        
        Porcentaje de la poblacion vulnerable por ingresos, 2008 - 2018
        * Dataset: Porcentaje, número de personas y carencias promedio por indicador de pobreza, según entidad federativa, 2008-2018, parte II
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/da89fadd-0f0e-425a-a7bb-154d091a51d7
        
        Porcentaje de la poblacion no pobre y no vulnerable, 2008 - 2018
        * Dataset: Porcentaje, número de personas y carencias promedio por indicador de pobreza, según entidad federativa, 2008-2018, parte II
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/da89fadd-0f0e-425a-a7bb-154d091a51d7
        
        Porcentaje de la poblacion no economicamente activa sin acceso a la seguridad social
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte III
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/ad82ec1d-13a4-470d-a443-a25b280aa8f9

        Porcentaje de la poblacion de 65 años o mas sin acceso a la seguridad social
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte III
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/ad82ec1d-13a4-470d-a443-a25b280aa8f9
        
        Porcentaje de la poblacion ocupada sin acceso a la seguridad social
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte III
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/ad82ec1d-13a4-470d-a443-a25b280aa8f9

        Porcentaje de la poblacion en viviendas con hacinamiento
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte IV
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/eabbfe33-feac-4568-bfa1-fa9c46014554

        Porcentaje de la poblacion en viviendas con techos de material endeble
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte IV
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/eabbfe33-feac-4568-bfa1-fa9c46014554

        Porcentaje de la poblacion en viviendas con pisos de tierra
        * Dataset: Porcentaje y número de personas en los componentes de los indicadores de carencia social, según entidad federativa, 2008-2018, parte IV
        * Enlace: https://datos.gob.mx/busca/dataset/indicadores-de-pobreza-2008-2018-nacional-y-estatal/resource/eabbfe33-feac-4568-bfa1-fa9c46014554

        Indice de libertad económica
        * Dataset: Table 3.3b: Mexico—Economic Freedom at the All-Government Level, 2003–2017
        * Enlace: https://www.fraserinstitute.org/sites/default/files/economic-freedom-of-north-america-2019-US-edition.pdf

        ''')
])
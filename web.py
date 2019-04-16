import pandas as pd
import numpy as np
import matplotlib.pyplot as ply
import seaborn as sns
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup
notarios = []
states = [
    'baja_california',
    'baja_california_sur',
    'chihuahua',
    'coahuila',
    'nuevo_leon',
    'tamaulipas',
    'sonora',
    'sinaloa',
    'durango',
    'zacatecas',
    'san_luis_potosi',
    'guanajuato',
    'aguascalientes',
    'jalisco',
    'queretaro',
    'michoacan',
    'veracruz',
    'quintana_roo',
    'yucatan',
    'campeche',
    'chiapas',
    'tabasco',
    'oaxaca',
    'guerrero',
    'puebla',
    'cdmx',
    'nayarit',
    'colima',
    'hidalgo',
    'estado_de_mexico',
    'tlaxcala',
    'morelos'
]

for state in states:
    file = state + ".html"
    url = "http://www.notarios.com.mx/index_new2_StateGov.asp?Estado=AGUASCALIENTES"
    html = open(file)
    html_url = urlopen(url)

    soup = BeautifulSoup(html, 'lxml')
    type(soup)

    rows = soup.find_all('div', class_="mpc-cubebox-side__content")

    list_rows = []
    cells = []
    for row in rows:
        cells = (row.find_all('p'))
        str_cells = str(cells)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '',str_cells))
        list_rows.append(clean2)
    
    i = 0
    while i < len(list_rows):
        if i % 2 == 0 & i < len(list_rows):
            list_rows[i] = list_rows[i] + "," + (list_rows[i + 1])
            notarios.append(list_rows[i])
            #notarios.append(np.concatenate((list_rows[i], list_rows[i + 1][0]), axis=None))
        i += 1

df = pd.DataFrame(notarios)
df1 = df[0].str.split(',', expand=True)
df1[0] = df1[0].str.strip('[')
df1[0] = df1[0].str.strip(']')
df1[7] = df1[7].str.strip(']')
df1[8] = df1[8].str.strip('[')
df1[8] = df1[8].str.strip(']')
df1[9] = df1[9].str.strip('[')
df1[9] = df1[9].str.strip(']')
df1[9] = df1[9].str.strip('(')
df1[9] = df1[9].str.replace('javascript:mostrarMail', ',')
df1[9] = df1[9].str.strip("'")
df1[9] = df1[9].str.split(',', '1')

df1[11] = df1[11].str.strip(']')
df1[11] = df1[11].str.split(";")
df1[11] = df1[11].str[1]
df1[10] = df1[10].str.split("'", '1')
df1.drop(df1.columns[[9, 10]], axis=1, inplace=True)

df1.to_csv(r'notarios.csv')




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 12:56:48 2021

@author: jack
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from pandas.plotting._matplotlib import converter
converter.register()

with open('dados_obitos.txt','r') as f:
    content = f.read()
   
d = json.loads(content)

dados = []
for i in d["rows"]:
    dados.append(i["columns"])
   
df = pd.DataFrame(dados,columns=['registro','cidade','genero','idade','obito'])

df['idade'] = df['idade'].astype('int')

df['datex'] = df['registro'].map(lambda x: datetime.datetime.strptime(str(x), "%d/%m/%Y"))

df.set_index('datex',inplace=True)

# print(df)

def classify(data):
    l = list(data)
    out = {}
    for i in set(l):
        i = int(i)
        out[i] = l.count(i)
    # print(out)
    return out

df2 = pd.DataFrame(df.groupby('datex')['idade'].apply(classify)).rename(columns={'datex':'sum'}).reset_index()

#print(df2)

fig = plt.figure()
fig = plt.figure(figsize = (12, 8), dpi=80)
ax = fig.add_subplot(111)#, projection='3d')

plt3d = ax.scatter(df2['level_1'],df2['idade'])

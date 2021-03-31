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
import numpy as np

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

df2 = pd.DataFrame(df.groupby('datex')['idade'].apply(classify)).rename(columns={'datex':'date','level_1':'idade','idade':'qtd'}).reset_index()


new = pd.DataFrame()

new['date'] = [x.date() for x in df2['datex']]
new['idade'] = [x for x in df2['level_1']]
new['qtd'] = [x for x in df2['qtd']]

pv = new.pivot(index='date', columns='idade', values=  'qtd')
pv = pv.fillna(0.0)

print(pv)

xx, yy = np.mgrid[0:len(pv.index),0:len(pv.columns)]

fig = plt.figure()
ax = fig.add_subplot(111)#, projection='3d')

#ax.plot_surface(xx, yy, pv.values, cmap='jet', rstride=1, cstride=10)
#ax.plot_surface(xx, yy, pv.values, cmap='jet', linewidth=5)
#ax.scatter(xx, yy, pv.values,c=pv.values, cmap='plasma')

c = ax.pcolormesh(xx,yy,pv.values,vmin=np.min(pv.values), \
                  vmax=np.max(pv.values),cmap='plasma', \
                  alpha=0.5) 
fig.colorbar(c, ax=ax)   


ax.grid(False)

dates = [x.strftime('%Y-%m-%d') for x in pv.index]
idades = [str(x) for x in pv.columns]

# Setting a tick every fifth element seemed about right
ax.set_xticks(xx[::15,0])
ax.set_xticklabels(dates[::15])
ax.set_yticks(yy[0,::10])
ax.set_yticklabels(idades[::10])

ax = plt.gca()
plt.gcf().autofmt_xdate()

plt.show()

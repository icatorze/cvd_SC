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


with open('dados_obitos.txt','r') as f:
    content = f.read()
   
d = json.loads(content)

dados = []
for i in d["rows"]:
    dados.append(i["columns"])
   
df = pd.DataFrame(dados,columns=['registro','cidade','genero','idade','obito'])

df['idade'] = df['idade'].astype('int')

ix = df['idade'].max()

ax1 = plt.gca()

df.plot.hist(y='idade', bins=ix, ax=ax1, label='Total',alpha=.1)

df.loc[(df['genero']=='Masculino')].plot.hist(y='idade',bins=ix,ax=ax1, label='Homens', alpha=.5)

df.loc[(df['genero']=='Feminino')].plot.hist(y='idade',bins=ix,ax=ax1, label='Mulheres', alpha=.5)


fig2, ax2 = plt.subplots()
df2 = pd.DataFrame()
df2['homens'] = df.loc[(df['genero']=='Masculino')]['idade'].value_counts().astype(int)
df2['homens'] = df2['homens'].fillna(0)
df2['mulheres'] = df.loc[(df['genero']=='Feminino')]['idade'].value_counts().astype(int)
df2['mulheres'] = df2['mulheres'].fillna(0)

df2['ratio'] = df2['homens']/df2['mulheres']

df2 = df2.sort_index()
#print(df2)

df2['ratio'].plot.bar(y='ratio',ax=ax2,label='Relacao')
#print(df2['ratio'].mean())

fig3, ax3 = plt.subplots()
df3 = pd.DataFrame()
df3 = df
df['datex'] = df['registro'].map(lambda x: datetime.datetime.strptime(str(x), "%d/%m/%Y"))

df3['octos'] = df.loc[(df['idade']>=80)]['idade']
df3['heptas'] = df.loc[(df['idade']>=70) & (df['idade']<80)]['idade']
df3['hexas'] = df.loc[(df['idade']>=60) & (df['idade']<70)]['idade']
df3['pentas'] = df.loc[(df['idade']>=50) & (df['idade']<60)]['idade']
df3['economic'] = df.loc[(df['idade']>=18) & (df['idade']<50)]['idade']
df3['menores'] = df.loc[(df['idade']<18)]['idade']
#df3['registro'] = df['registro']

def mean_deaths(dfg, grupo):
    label = "media {}".format(grupo)
    ratio = 100.*dfg.groupby('datex').count()[grupo]/dfg.groupby('datex').count()['idade']
    return ratio,ratio.ewm(7).mean(),label

grupos = ['octos','heptas','hexas','pentas','economic','menores']

for g in grupos:
    r,m,l = mean_deaths(df3, g)
    r.plot(alpha=.2,ax=ax3,label=g)
    m.plot(alpha=1,ax=ax3,label=l)

plt.grid()
plt.legend()

print(deathsdf)
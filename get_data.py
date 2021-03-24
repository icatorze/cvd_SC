#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 10:43:59 2021

@author: jack
"""

from bs4 import BeautifulSoup
import requests
import ast as pyast
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
import json
 
resp = requests.get("https://flo.uri.sh/visualisation/3561978/embed",verify=False)
 
html = resp.content
soup = BeautifulSoup(html, "html.parser") #features="lxml")
 
script_tags = soup.find_all("script",{'src': False})

tag = script_tags[3].string
#print(tag)

parser = Parser()
tree = parser.parse(tag)
#

for node in nodevisitor.visit(tree):
#    print(node)
    if isinstance(node, ast.VarDecl) and node.identifier.value == '_Flourish_data':
#        dados.append(node.to_ecma())
        dados = node.to_ecma().split('=')[1]
   
with open('dados_obitos.txt','+w') as f:
    f.write(str(dados))



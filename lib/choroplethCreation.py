#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:21:14 2019

@author: tal.wanish
"""

import pandas as pd
from bs4 import BeautifulSoup

path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/countyData.csv')
countyData = pd.read_csv(path, engine='python')
path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/graphics/USA_Counties_with_FIPS_and_names.svg')
svg = open(path, 'r').read()
soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'], features='lxml')
# Find counties
paths = soup.findAll('path')
colors = ["#f1eef6", "#bdc9e1", "#74a9cf", "#2b8cbe", "#045a8d"]
# County style
path_style='''font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1; 
    stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;
    marker-start:none;stroke-linejoin:bevel;fill:'''
    
# Color the counties based on share market cap rate
for p in paths:
     
    if p['id'] not in ["State_Lines", "separator"]:
        # pass
        try:
            marketCap = countyData[countyData['county']==int(p['id'].split('_')[1])]['share_market_cap'].values[0]
        except:
            continue

        if marketCap > countyData['share_market_cap'].quantile(.8):
            color_class = 4
        elif marketCap > countyData['share_market_cap'].quantile(.6):
            color_class = 3
        elif marketCap > countyData['share_market_cap'].quantile(.4):
            color_class = 2
        elif marketCap > countyData['share_market_cap'].quantile(.2):
            color_class = 1
        else:
            color_class = 0
 
        color = colors[color_class]
        p['style'] = path_style + color
        
output = open(os.path.normpath(str(os.getcwd()).split('lib')[0]+'/graphics/share_market_cap.svg'), "w")
output.write(soup.prettify())
output.close()


          



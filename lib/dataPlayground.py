#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:58:11 2019

for pulling data

@author: tal.wanish
"""
import pandas as pd
import numpy as np


def getCity(cityName, state, df):
    cityChoices = df[df['PO_NAME']==cityName]
    cityChoices = cityChoices[cityChoices['STATE']==state]
    grouped = cityChoices.groupby('PO_NAME').agg({
            'STATE':'min', 'ZCTA':'max', 'brewery_count':'sum', 'popDrinking': 'sum',
            'median_income':'mean', 'purchase_power':'mean',
            'brewery_capacity':'sum'})
    tC= groupCities(df)
    
    
    if grouped['STATE'].size==0:
        print ('We do not have any records on ' + cityName + ', ' + state)
    else:
        
        grouped['tot_market_cap']=grouped['popDrinking']*grouped['purchase_power']
        grouped['carrying_cap_ratio']=grouped['brewery_capacity']/(
            1+((grouped['brewery_capacity']-(grouped['brewery_count']+1))/(grouped['brewery_count']+1)))
        grouped['carrying_cap_ratio']=(grouped['brewery_capacity']-np.abs(
                grouped['brewery_capacity']-grouped['carrying_cap_ratio']
                ))/grouped['brewery_capacity']
        grouped['share_market_cap']=grouped['tot_market_cap']*grouped['carrying_cap_ratio']
        grouped['split_market_cap']=grouped['tot_market_cap']/(grouped['brewery_count']+1)
        x = grouped.share_market_cap.item()
        y = grouped.split_market_cap.item()
        print(grouped.head())
        print("Share: " + str(tC[tC['share_market_cap']>x]['share_market_cap'].size)+"/"+str(tC['share_market_cap'].size))
        print("Split: " + str(tC[tC['split_market_cap']>y]['split_market_cap'].size)+"/"+str(tC['split_market_cap'].size))
        
    return

def getZip(zipCode, df):
    pd.set_option('display.expand_frame_repr', False)
    x = df[df['ZCTA']==zipCode].share_market_cap.item()
    y = df[df['ZCTA']==zipCode].split_market_cap.item()
    print(df[df['ZCTA']==zipCode])
    print("Share: " + str(df[df['share_market_cap']>x]['share_market_cap'].size)+"/"+str(df['share_market_cap'].size))
    print("Split: " + str(df[df['split_market_cap']>y]['split_market_cap'].size)+"/"+str(df['split_market_cap'].size))
    
    return

def groupCities(df):
    tC = df.groupby(['PO_NAME', 'STATE']).agg({
            'ZCTA':'max', 'brewery_count':'sum', 'popDrinking': 'sum',
            'median_income':'mean', 'purchase_power':'mean',
            'brewery_capacity':'sum'})
    tC['tot_market_cap']=tC['popDrinking']*tC['purchase_power']
    tC['carrying_cap_ratio']=tC['brewery_capacity']/(
        1+((tC['brewery_capacity']-(tC['brewery_count']+1))/(tC['brewery_count']+1)))
    tC['carrying_cap_ratio']=(tC['brewery_capacity']-np.abs(
            tC['brewery_capacity']-tC['carrying_cap_ratio']
            ))/tC['brewery_capacity']
    tC=tC.fillna(0.5)
    tC['share_market_cap']=tC['tot_market_cap']*tC['carrying_cap_ratio']
    tC['split_market_cap']=tC['tot_market_cap']/(tC['brewery_count']+1)
    return tC
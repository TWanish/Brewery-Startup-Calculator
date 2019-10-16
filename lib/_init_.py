import pandas as pd
import numpy as np
import os
from tableCreation import joinZip, joinData
from dataPlayground import getZip, getCity, groupCities, groupCounties

### Init
pd.set_option('display.max_columns', 15)
try:
    path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/breweryData.json')
except:
    print('path not found')

data = pd.read_json(path)
data['zip code'] = data['zip code'].astype(str)
pathZipCW = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/zipZctaCrosswalk.csv')
zipCW = pd.read_csv(pathZipCW, engine='python').rename(columns = {'ZIP_CODE' : 'zip code'})
zipCW['zip code'] = zipCW['zip code'].astype(str)
withZip = joinZip(data, zipCW)
withZip = withZip.dropna(axis=0, subset=['ZCTA'])
withZip['ZCTA'] = withZip['ZCTA'].astype(int)
pathCountyCW = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/zctaCountyCrosswalk.csv')
countyCW = pd.read_csv(pathCountyCW, engine='python').rename(columns = {'zip' : 'ZCTA'}).reset_index().rename(index=str, columns={"index": "ZCTA", "ZCTA": "county"})


pathHousing = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/popData.csv')
population = pd.read_csv(pathHousing, engine='python').rename(columns = {'GEO.id2' : 'ZCTA'})
withPopulation = joinData(withZip, population).fillna(0)

pathLand = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/geoDataZCTA.csv')
landData = pd.read_csv(pathLand, engine='python').rename(columns = {'GEOID' : 'ZCTA',
                                                                      'ALAND_SQMI' : 'land_area_sqmi'})

### Determine frequency of brewery counts per ZCTA/State

zipTotals = withPopulation[['ZCTA', 'popDrinking', 'brewery size']].groupby('ZCTA').agg(
        {'brewery size':'count', 'popDrinking': 'mean'}
        ).rename(index=str, columns={'brewery size': 'brewery_count'})

zipTotals['brewery_count']=zipTotals['brewery_count'].astype(int)
zipTotals=zipTotals.replace(np.inf, 0).reset_index()
zipTotals['ZCTA'] = zipTotals.astype({'ZCTA':'int'})
zipByCount = joinData(zipCW, zipTotals)[['PO_NAME', 'STATE',
                     'ZCTA', 'brewery_count']].fillna(0).sort_values('ZCTA')
zipByCount = joinData(zipByCount, population[['ZCTA', 'popDrinking']]).fillna(0)
zipByCount['BpC'] = zipByCount['brewery_count']/zipByCount['popDrinking']
zipByCount = zipByCount.drop_duplicates(subset='ZCTA').reset_index()
#print(zipByCount[zipByCount['popDrinking']>10000].sort_values('BpC').head(5)) For determining top/bottom performers

### Add spending power data
pathIncome = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/medianIncomeOnly.csv')
income = pd.read_csv(pathIncome, engine='python').rename(columns = {'GEO.id2' : 'ZCTA',
                                                                    'HC01_EST_VC13' : 'median_income'})

withIncome = joinData(zipByCount, income).fillna(0)

pathHousing = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/medianHousingOnly.csv')
housing = pd.read_csv(pathHousing, engine='python').rename(columns = {'GEO.id2' : 'ZCTA',
                                                                    'HD01_VD01' : 'median_housing'})

### Determine best location
withLand = joinData(withIncome, landData[['ZCTA', 'land_area_sqmi']]).fillna(0) #Join here to not lose data
withCounty = joinData(withLand, countyCW).fillna(0)
withCounty['county']= withCounty['county'].astype(int)
withHousing = joinData(withCounty, housing).fillna(0) #Join here to not lose data
withHousing['brewery_density']=withHousing['brewery_count']/withHousing['land_area_sqmi']
withHousing['median_housing'] = withHousing['median_housing']*12
withHousing['purchase_power'] = (withHousing['median_income']-withHousing['median_housing'])/(
        pow(withHousing['median_housing'],.463)
        )
withHousing['prod_capacity']=withHousing['popDrinking']*0.838 #assume .838bbl consumption yearly https://www.usatoday.com/story/money/personalfinance/2018/05/02/which-states-residents-drink-most-beer/569430002/
withHousing['brewery_capacity']=withHousing['prod_capacity']/1000 #assume 1000bbl production yearly https://www.brewbound.com/news/beer-business-finance-breaking-down-the-taproom-focused-brewery-model
withHousing['brewery_capacity']=(withHousing['brewery_capacity']*.127).astype(int) #assume 12.7% of beer consumed in an area is craft https://www.brewersassociation.org/statistics/national-beer-sales-production-data/
withHousing['tot_market_cap']=withHousing['purchase_power']*withHousing['popDrinking']
withHousing['carrying_cap_ratio']=withHousing['brewery_capacity']/(
        1+((withHousing['brewery_capacity']-(withHousing['brewery_count']+1))/(
                withHousing['brewery_count']+1))
        *np.exp(-.5)) #from https://sites.math.northwestern.edu/~mlerma/courses/math214-2-04f/notes/c2-logist.pdf
withHousing['carrying_cap_ratio']=(withHousing['brewery_capacity']-np.abs(
        withHousing['brewery_capacity']-withHousing['carrying_cap_ratio']))/withHousing['brewery_capacity']
withHousing['share_market_cap']=withHousing['tot_market_cap']*withHousing['carrying_cap_ratio']
withHousing['split_market_cap']=withHousing['tot_market_cap']/(
        withHousing['brewery_count']+1)

impInfo = withHousing[['PO_NAME', 'STATE', 'ZCTA', 'county', 'popDrinking', 'brewery_count',
                       'median_income', 'purchase_power', 'land_area_sqmi',
                       'brewery_capacity', 'carrying_cap_ratio', 'share_market_cap',
                       'split_market_cap']].fillna(0).replace(np.inf,0)



getCity("Denver", "CO", impInfo)
#getZip(28277, impInfo)
#print(impInfo.sort_values('share_market_cap').tail())
#print(impInfo.sort_values('split_market_cap').tail())
tC = groupCounties(impInfo).reset_index()
tC['share_market_cap']=tC['share_market_cap'].astype(int)
tC['split_market_cap']=tC['split_market_cap'].astype(int)
tC['brewery_per_capita']=tC['brewery_count']/tC['popDrinking'].fillna(0).replace(np.inf,0)

tC.to_csv(os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/countyData.csv'))


#impInfo=impInfo[impInfo['brewery_capacity']>impInfo.brewery_count.astype(int)] #remove any city that has already hit their carrying capacity

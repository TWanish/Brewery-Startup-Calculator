import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from tableCreation import joinZip, joinData

### Init

try:
    path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/breweryData.json')
    path = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/breweryData.json')
except:
    print('path not found')

data = pd.read_json(path)

pathZipCW = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/zipZctaCrosswalk.csv')
zipCW = pd.read_csv(pathZipCW, engine='python').rename(columns = {'ZIP_CODE' : 'zip code'})

withZip = joinZip(data, zipCW)

pathIncome = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/medianIncomeOnly.csv')
income = pd.read_csv(pathIncome, engine='python').rename(columns = {'GEO.id2' : 'ZCTA',
                                                                    'HC01_EST_VC13' : 'median income'})

withIncome = joinData(withZip, income)

pathHousing = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/medianHousingOnly.csv')
housing = pd.read_csv(pathHousing, engine='python').rename(columns = {'GEO.id2' : 'ZCTA',
                                                                    'HD01_VD01' : 'median housing'})

withHousing = joinData(withIncome, housing)

pathHousing = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/popData.csv')
population = pd.read_csv(pathHousing, engine='python').rename(columns = {'GEO.id2' : 'ZCTA'})

withPopulation = joinData(withHousing, population).fillna(0)
### Determine frequency of brewery counts per ZCTA/State
zipTotals = withPopulation[['ZCTA', 'popDrinking', 'brewery size']].groupby('ZCTA').agg({'brewery size':'count',
                          'popDrinking': 'mean'}).rename(index=str, columns={'brewery size': 'brewery count'})
zipTotals['BpC'] = zipTotals['brewery count']/zipTotals['popDrinking']
zipTotals=zipTotals.replace(np.inf, 0).reset_index()
zipTotals['ZCTA'] = zipTotals.astype({'ZCTA': 'float'}).astype({'ZCTA':'int'})
zipByCount = joinData(zipCW, zipTotals)[['zip code', 'STATE', 'ZCTA', 'brewery count', 'popDrinking', 'BpC']].fillna(0).sort_values('STATE')
sns.set_style("darkgrid")

#f, statePlots = plt.subplots(8, 7,figsize=(48,27))
#for i, state in enumerate(zipByCount.STATE.unique()):
#    stateData = zipByCount.loc[zipByCount['STATE']==state]
#    stateCount = stateData['brewery count'].values
#    sns.distplot(stateCount, kde=False, bins=range(0,10), norm_hist=True, ax=statePlots[int(i/7), i%7]).set(xlim=(0,10),ylim=(0,1))
#    statePlots[int(i/7), i%7].set_title(state)
#    
#countHist = zipByCount['brewery count'].values
#f.savefig("foo.png")
#
#plt.figure()
#sns.distplot(countHist, kde=False, bins=range(0,10), norm_hist=True).set(xlim=(0,10),ylim=(0,1))
#plt.title("United States")




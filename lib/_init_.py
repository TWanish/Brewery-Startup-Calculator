import pandas as pd
import numpy as np
import os
from tableCreation import joinZip, joinIncome, joinHousing

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

withIncome = joinIncome(withZip, income)

pathHousing = os.path.normpath(str(os.getcwd()).split('lib')[0]+'/data/medianHousingOnly.csv')
housing = pd.read_csv(pathHousing, engine='python').rename(columns = {'GEO.id2' : 'ZCTA',
                                                                    'HD01_VD01' : 'median housing'})

withHousing = joinHousing(withIncome, housing)

print(withHousing.head(20))

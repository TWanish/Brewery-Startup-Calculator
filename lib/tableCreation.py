import pandas as pd
import numpy as np

### Data and table manipulation

def joinZip(dataTable, zipCrosswalk):
    zipCodes = []
    for code in zipCrosswalk['zip code'].values:
        code = "00000"+str(code)
        zipCodes.append(code[len(code)-5:len(code)])
    zipCrosswalk['zip code']=zipCodes

    data = pd.merge(dataTable, zipCrosswalk, how='left', on='zip code').drop(['PO_NAME','STATE'],
                                                                 axis=1)
    return data

def joinIncome(dataTable, incomeData):
    data = pd.merge(dataTable, incomeData, how='left', on='ZCTA')

    return data

def joinHousing(dataTable, housingData):
    data = pd.merge(dataTable, housingData, how='left', on='ZCTA')

    return data

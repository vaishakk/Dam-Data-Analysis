"""
Created on Fri Aug 18 13:38:33 2017

@author: tango
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

url = "http://sldckerala.com/index.php" #The State Load Dispatch Centre website
browser = RoboBrowser(history=True) #Initialize browser
#Fetch data from 1st Aug to 31st Aug (heavy floods occurred between 15th and 20th)
fromDay = 1 
toDay = 31
#month = 8
day = np.arange(fromDay,toDay+1)
dams = []
damLevelData = np.array([[[0]*8]*len(day)]*16,np.float64) #8 data-points, len(day) days and 16 dams
k = 0
for d in day:
    print('Collecting data for day '+str(d))
    #Set form data
    date1 = '2018-08/20-' + str(d)
    data = {'txtDate': '1534789800',
            'date1': date1,
            'date1_dp': '1',
            'date1_day':str(d),
            'date1_month': '08', 
            'date1_year':  '2018',
            'sbtstore': 'SHOW'}

    browser.open(url,method = 'post',data = data)#Open page
    page = browser.parsed
    #Fetch table data
    table = page.find('table', attrs={'class':'display'})
    if not table:
        continue #Skip empty table
    rows = table.find_all('tr')
    #print(rows)
    #Extract row data
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        #print(cols)
        data.append(cols)
        #data.append([ele for ele in cols if ele]) 
    #print(data)
    levels = pd.DataFrame(data)
    #print(levels.loc[2:8,:])
    damData = pd.DataFrame(data=pd.concat([levels.loc[2:8,:],levels.loc[10:13,:],levels.loc[15:19,:]]),copy=True) #Refactoring data
    #colNames = ['Min.Draw Down Level(m)','Full Reservoir Level(m)','Full Reservoir Stg.(mcm)','Full Reservoir Stg(mu)','RESERVOIR','Level (m)','Effective Storage (mcm)','Storage (%)','Gen. Capability (mu) Gross','Gen. Capability (mu) Station','RainFall(mm)','Spill(mcm/day)','Inflow(mu)','Cum. IF for month mu',"Previous day's storage (%)",'Remarks']
    colName =  ['Day','Full Reservoir Level(m)','Full Reservoir Stg.(mcm)','Level (m)','Effective Storage (mcm)','RainFall(mm)','Spill(mcm/day)','Inflow(mu)']
    #print(len(cols))
    damData = pd.DataFrame(damData.values,columns = colNames) #Select columns
    
    if d == fromDay:
        #From day 1 data extract dam names
        dams.append(damData.iloc[:,4].values)
        dams = dams[0]
    #print(len(dams))
    for i in range(0,len(dams)):
        # Compile data per dam for all days
        damLevelData[i][k] = pd.to_numeric([d,damData.iloc[i,1],damData.iloc[i,2],damData.iloc[i,5],damData.iloc[i,6],damData.iloc[i,10],damData.iloc[i,11],damData.iloc[i,12]])
    k = k + 1
    #print(dams)
    damData.set_index('RESERVOIR',inplace=True)\
# Write data of each dam to excel file
for i in range(0,16):
    dd = pd.DataFrame(damLevelData[:][:][i],columns = colName)
    dd.set_index('Day',inplace=True)
    dd.fillna(0,inplace=True)
    dd.to_csv(dams[i]+'.csv')
#print(damLevelData)
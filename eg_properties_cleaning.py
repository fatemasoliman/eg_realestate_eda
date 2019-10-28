import numpy as np
import pandas as pd
import re
import json
from scipy import stats
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
plt.style.use('ggplot')


#read in sraped data file
props_raw = pd.read_csv('propfinder.csv')
#props_raw.head()


#CLEAN ADDRES FIELDS
props_clean = props_raw
props_clean['type_fromaddress']= list(map(lambda x: x.find("for Sale in"), props_clean['address']))
props_clean['address2'] = props_clean.address.str.split("for Sale in")
props_clean[['type_fromaddress', 'a1']] = pd.DataFrame(props_clean.address2.values.tolist(), index = props_clean.index)
props_clean['a2'] = props_clean.a1.str.split(',')
props_clean[['a2', 'a3']] = pd.DataFrame(props_clean.a2.values.tolist(), index = props_clean.index)
props_clean = props_clean.drop(['ref', 'address2', 'a1'],1)


#CLEAN BED AND BATH COLUMNS
props_clean['bed2'] = props_clean.bed.str.split("+")
props_clean['bed'] = list(map(lambda x: x[0] if isinstance(x, list) else x, props_clean['bed2']))
props_clean['bed'] = props_clean['bed'].str.replace('+', '')
props_clean['bed'] = props_clean['bed'].str.replace('studio', '0')
props_clean['bed'] = props_clean['bed'].str.replace('N/A ', '')
props_clean['bath'] = props_clean['bed'].str.replace('+', '')


#CLEAN SQM COLUMNS
props_clean['sqm'] = props_clean['sqm'].str.replace('\n', '')
props_clean['sqm2'] = props_clean.sqm.str.split('/')
props_clean[['sqft', 'sqm']] =  pd.DataFrame(props_clean.sqm2.values.tolist(), index = props_clean.index)
props_clean['sqft']= props_clean['sqft'].str.replace('sqft', '').str.strip()
props_clean['sqm']= props_clean['sqm'].str.replace('sqm', '').str.strip()
props_clean['sqft']= props_clean['sqft'].str.replace(',', '').str.strip()
props_clean['sqm']= props_clean['sqm'].str.replace(',', '').str.strip()
props_clean = props_clean.drop('sqm2',1)

props_clean.sqm = pd.to_numeric(props_clean.sqm)

props_clean.sqm = pd.to_numeric(props_clean.sqm)
props_clean.bed = pd.to_numeric(props_clean.bed)
props_clean.bath = pd.to_numeric(props_clean.bath)


#props_clean.describe()

#EXTRACT LAT LONGS
props_clean.json2 = list(map(lambda x: json.loads(x), props_clean.json2))
props_clean['geo'] = list(map(lambda x: x[1]['geo'].values(), props_clean.json2))
props_clean.geo = list(map(lambda x: list(x), props_clean.geo))
props_clean['lat'] = list(map(lambda x: x[1], props_clean.geo))
props_clean['long'] = list(map(lambda x: x[2], props_clean.geo))


props_clean = props_clean.drop({'json1', 'json2'}, 1)

#CLEAN PRICE

props_clean.price = props_clean.price.str.replace(',', '').str.strip()
props_clean.price = pd.to_numeric(props_clean.price)


#CREATE PSQM FIELD
props_clean['psqm'] = props_clean.price/props_clean.sqm

props_clean.psqm.describe()
props_clean.sort_values(by = ['psqm'])

props_clean = props_clean.drop(props_clean.loc[props_clean.psqm == 1].index)


#CLEAN PROP TYPE COLUMN
props_clean['proptype'] = props_clean['proptype'].str.replace('iVilla', 'Villa')
props_clean = props_clean.drop(props_clean.loc[props_clean.proptype == 'Compound'].index)



#################MATCHING COMPOUNDS AND DEVELOPERS
#compounds = props_compounds.price.agg("count").sort_values(ascending = False)
#compounds.to_csv('compounds.csv')

developers = pd.read_csv('developer_lookup.csv')

props_clean = props_clean.merge(developers,left_on = 'a2' , right_on = 'Compound')
props_clean['Developer'] = props_clean['Developer'].str.strip()

developers_df = props_clean[['Developer', 'price', 'psqm']].groupby('Developer').agg({'Developer' : ['count'], 'price': ['mean'], 'psqm' : ['mean']})
developers_df.columns = list(map(''.join, developers_df.columns.values))
developers_df  = developers_df.sort_values(by = ['Developercount'],ascending = False)
developers_df = developers_df.reset_index()
developers_df = developers_df.drop(0)
top10devs = developers_df[:-31]
top10devs

props_top10 = props_clean.loc[props_clean.Developer.isin(top10devs['Developer'])]
props_top10['Developer'] = props_top10['Developer'].str.replace('Hyde Park Developments', 'Hyde Park')
props_top10['Developer'] = props_top10['Developer'].str.replace('Talaat Moustafa Group', 'Talaat Moustafa')

###to csv

props_top10.to_csv('props_top10.csv')
props_clean.to_csv('props_clean.csv')


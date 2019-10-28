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

props_top10 = pd.read_csv('props_top10.csv')
props_clean = pd.read_csv('props_clean.csv')

sns.set_style("white")
sns.despine()
ylabels = range(0, 120, 20)

#P/SQM SCATTER PLOT

'''
props_clean_scatter = props_clean[['price', 'sqm']]

props_clean_scatter = props_clean_scatter.loc[props_clean_scatter.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)]

sns.despine()

scat1 = sns.regplot(x="sqm", y="price", data=props_clean_scatter, fit_reg = False)
plt.xlabel('SqM')
plt.ylabel('Price (millions)')

ylabels = range(0, 120, 20)
scat1.set(yticklabels=ylabels)
sns.despine()
plt.savefig('scat1.eps')


#LOG PRICE HISTOGRAM
log_price = np.log(props_clean['price'])
sns.distplot(log_price)
plt.xlabel('Log(Price)')
plt.xlim(10,20)
sns.despine()
plt.savefig('logp_hist.eps')
'''

props_clean2 =props_clean.drop(props_clean.loc[props_clean.proptype == "Bungalow"].index)
'''
typeprice_boxplot = sns.boxplot(x="proptype", y="price", data=props_clean2)
plt.ylim(0,3e7)
plt.xlabel('Property Type')
plt.ylabel('Price (millions)')
typeprice_boxplot.set(yticklabels=range(0,35,5))
sns.despine()
plt.savefig('typeprice_boxplot.eps')


props_box = props_clean2[['price', 'psqm', "proptype"]]

#props_box = props_box.drop(props_box.loc[props_box.pqsm.apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)]
q_psqm = props_box["psqm"].quantile(0.95)
props_box=props_box[props_box["psqm"] < q_psqm]

typepsqm_boxplot = sns.boxplot(x="proptype", y="psqm", data=props_box)
#plt.xlabel('Property Type')
plt.ylabel('Price/SqM')
#typepsqm_boxplot.set(yticklabels=range(0,35,5))
sns.despine()
plt.savefig('typepsqm_boxplot.eps')

'''

#props_top10['logpsqm'] = np.log(props_top10['psqm'])

q_psqm = props_top10["psqm"].quantile(0.95)
props_top10_filtered=props_top10[props_top10["psqm"] < q_psqm]
a= props_top10_filtered[['Developer', 'psqm']].groupby('Developer').agg("mean").sort_values("psqm", ascending = False)





sns.set(font_scale = 0.8)
sns.set_style("white")
sns.boxplot(x="Developer", y="psqm", data=props_top10_filtered, order = a.index)
plt.xlabel('Developer')
plt.ylabel('Price/SqM')
sns.despine()
plt.savefig('typepsqm_boxplot.eps')
#plt.ylim(4,15)

plt.show()
import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd


# "Reported_Date","HA","Sex","Age_Group","Classification_Reported"
BC_CASES_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
 
pop_groups = [
    {"Group": "<10",   "Population": 457525, "Percent": 0.10},
    {"Group": "10-19", "Population": 492840, "Percent": 0.11},
    {"Group": "20-29", "Population": 590560, "Percent": 0.13},
    {"Group": "30-39", "Population": 607340, "Percent": 0.13},
    {"Group": "40-49", "Population": 617410, "Percent": 0.13},
    {"Group": "50-59", "Population": 709300, "Percent": 0.15},
    {"Group": "60-69", "Population": 611615, "Percent": 0.13},
    {"Group": "70-79", "Population": 347010, "Percent": 0.07},
    {"Group": "80-89", "Population": 172765, "Percent": 0.04},
    {"Group": "90+",   "Population": 41685,  "Percent": 0.01}
]

df = pd.read_csv(BC_CASES_URL)

ct = pd.crosstab(index=df['Reported_Date'], columns=df['Age_Group'])
ct.reset_index(inplace=True)

ct['Smoothed<10']   = ct['<10'].rolling(7).mean()
ct['Smoothed10-19'] = ct['10-19'].rolling(7).mean()
ct['Smoothed20-29'] = ct['20-29'].rolling(7).mean()
ct['Smoothed30-39'] = ct['30-39'].rolling(7).mean()
ct['Smoothed40-49'] = ct['40-49'].rolling(7).mean()
ct['Smoothed50-59'] = ct['50-59'].rolling(7).mean()
ct['Smoothed60-69'] = ct['60-69'].rolling(7).mean()
ct['Smoothed70-79'] = ct['70-79'].rolling(7).mean()
ct['Smoothed80-89'] = ct['80-89'].rolling(7).mean()
ct['Smoothed90+']   = ct['90+'].rolling(7).mean()

fig1 = plt.figure(1, figsize=(8, 5))

plt.title('Cases by Age', fontsize='large')
plt.xlabel="Date"
plt.ylabel="Number"

ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
plt.plot(ct['Reported_Date'], ct['Smoothed<10'],   label='<10')
plt.plot(ct['Reported_Date'], ct['Smoothed10-19'], label='10-19')
plt.plot(ct['Reported_Date'], ct['Smoothed20-29'], label='20-29')
plt.plot(ct['Reported_Date'], ct['Smoothed30-39'], label='30-39')
plt.plot(ct['Reported_Date'], ct['Smoothed40-49'], label='40-49')
plt.plot(ct['Reported_Date'], ct['Smoothed50-59'], label='50-59')
plt.plot(ct['Reported_Date'], ct['Smoothed60-69'], label='60-69')
plt.plot(ct['Reported_Date'], ct['Smoothed70-79'], label='70-79')
plt.plot(ct['Reported_Date'], ct['Smoothed80-89'], label='80-89')
plt.plot(ct['Reported_Date'], ct['Smoothed90+'],   label='90+')
plt.legend()
# plt.legend(['90+', '80-89', '70-79', '60-69', '50-59', '40-49', '30-39', '20-29', '10-19', '<10'])
plt.grid(b=True, which='major')
plt.show()
plt.close()

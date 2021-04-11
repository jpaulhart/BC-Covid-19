#!/usr/bin/env python3
#
# provinces.py
#
# provinces.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""bccases page shows Canadian Provinces Cases"""
import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st
import awesome_streamlit as ast

import constants as cn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""

    dfAdmin = pd.read_csv(cn.CANADA_VACCINATION_ADMINSTERED)
    dfAdmin['date_vaccine_administered64']= pd.to_datetime(dfAdmin['date_vaccine_administered'], format='%d-%m-%Y')
    dfAdmin['date_vaccine_administered'] = dfAdmin['date_vaccine_administered64'].dt.strftime('%Y-%m-%d')
    dfAdmin = dfAdmin.sort_values(['date_vaccine_administered64'], ascending=[True])
    dfAdmin['cumulative_avaccine_mean'] = dfAdmin['cumulative_avaccine'].rolling(7).mean()

    dfCompl = pd.read_csv(cn.CANADA_VACCINATION_COMPLETED)
    dfCompl['date_vaccine_completed64']= pd.to_datetime(dfCompl['date_vaccine_completed'], format='%d-%m-%Y')
    dfCompl['date_vaccine_completed'] = dfCompl['date_vaccine_completed64'].dt.strftime('%Y-%m-%d')
    dfCompl = dfCompl.sort_values(['date_vaccine_completed64'], ascending=[True])
    dfCompl['cumulative_cvaccine_mean'] = dfCompl['cumulative_cvaccine'].rolling(7).mean()

    dfDistr = pd.read_csv(cn.CANADA_VACCINATION_DISTRIBUTED)
    dfDistr['date_vaccine_distributed64']= pd.to_datetime(dfDistr['date_vaccine_distributed'], format='%d-%m-%Y')
    dfDistr['date_vaccine_distributed'] = dfDistr['date_vaccine_distributed64'].dt.strftime('%Y-%m-%d')
    dfDistr = dfDistr.sort_values(['date_vaccine_distributed64'], ascending=[True])
    dfDistr['cumulative_dvaccine_mean'] = dfDistr['cumulative_dvaccine'].rolling(7).mean()

    dfLastDate = dfDistr.tail(n=1)
    last_date = dfLastDate['date_vaccine_distributed'].values[0]

    dfFirstDate = dfDistr.head(n=1)
    first_date = dfFirstDate['date_vaccine_distributed'].values[0]

    date_range = f'Data range: {first_date} to {last_date}'

    st.title("Vaccinations by Day")
    cn.DATE_SPANS()

    writeProvinceAdmin(dfAdmin, dfDistr, dfCompl)

    writeProvinceGraph(dfAdmin, dfDistr, dfCompl, 'BC')
    writeProvinceGraph(dfAdmin, dfDistr, dfCompl, 'Alberta')
    writeProvinceGraph(dfAdmin, dfDistr, dfCompl, 'Ontario')
    writeProvinceGraph(dfAdmin, dfDistr, dfCompl, 'Quebec')

def writeProvinceAdmin(dfAdmin, dfDistr, dfCompl):

    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)

    prov_pop = {
        "Canada":           38048738,
        "NL":               520438,
        "PEI":              159819,
        "Nova Scotia":      979449,
        "New Brunswick":    782078,
        "Quebec":           8575944,
        "Ontario":          14755211,
        "Manitoba":         1380935,
        "Saskatchewan":     1178832,
        "Alberta":          4436258,
        "BC":               5153039,
        "Yukon":            42192,
        "NWT":              45136,
        "Nunavut":          39407
    }

    dfLastOne = dfAdmin.tail(1)
    lastDate = dfLastOne['date_vaccine_administered64'].values[0]
    dfLastDates = dfAdmin[dfAdmin['date_vaccine_administered64'] == lastDate]

    provinces = []
    admin_pers = []
    all_accum = 0
    for index, row in dfLastDates.iterrows():
        province = row['province']
        admin_total = row['cumulative_avaccine']
        population = prov_pop[province]
        admin_per = admin_total / (population / 100)
        provinces.append(province)
        admin_pers.append(admin_per)
        all_accum += admin_total

    ca_pop = prov_pop['Canada']
    admin_per = all_accum / (ca_pop / 100)
    provinces.append('Canada')
    admin_pers.append(admin_per)

    dataCols = {'provinces':  provinces,
                'admin_percent': admin_pers
            }

    df = pd.DataFrame (dataCols, columns = ['provinces','admin_percent'])
    df = df.sort_values(['admin_percent'], ascending=[True])
    #print (df)

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title('Vaccinations Administered - Percent of Pop.', fontsize='large')
    plt.xlabel="Percent"
    plt.ylabel="Province"
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    #plt.ylabel("Calories Burned Per Day", fontsize=14, labelpad=15)

    #plt.xticks(rotation=45)
    ax = plt.gca()
    ax.barh(df['provinces'], df['admin_percent'], align='center',
            color='green', ecolor='black')

    for i, v in enumerate(df['admin_percent']):
        ax.text(v - 3, i - .25, str("{:10.2f}".format(v)), color='green', fontweight='bold')

    #ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

    #plt.plot(df['admin_percent'], df['provinces'], label='Percent Administered')
    plt.grid(b=True, which='major')

    st.pyplot(fig1)
    #plt.show()
    plt.close()

def writeProvinceGraph(dfAdmin, dfDistr, dfCompl, province):
    dfAdmin = dfAdmin[dfAdmin['province'] == f'{province}']
    dfDistr = dfDistr[dfDistr['province'] == f'{province}']

    # ------------------------------------------------------------------------

    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title(f'{province} Vaccines', fontsize='large')
    plt.xlabel="Date"
    plt.ylabel="Number"

    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))

    plt.bar(dfDistr['date_vaccine_distributed'], dfDistr['cumulative_dvaccine'], label=f'{province} Vaccines Distributed')
    plt.bar(dfAdmin['date_vaccine_administered'], dfAdmin['cumulative_avaccine'], label=f'{province} Vaccines Administered')
    plt.bar(dfCompl['date_vaccine_completed'], dfCompl['cumulative_cvaccine'], label=f'{province} Vaccines Completed')
    plt.legend(['Distributed','Administered','Completed'])
    plt.grid(b=True, which='major')
    
    st.pyplot(fig1)
    plt.close()

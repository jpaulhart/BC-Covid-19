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
    st.markdown(f'<div style="font-size: 9pt">Case Dates: {cn.FIRST_DATE} to {cn.LAST_DATE}</div>\n', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 9pt">BCCDC Dates: {cn.BCCDC_FIRST_DATE} to {cn.BCCDC_LAST_DATE}</div>\n', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 9pt">Vaccination Dates: {cn.VAX_FIRST_DATE} to {cn.VAX_LAST_DATE}</div>\n', unsafe_allow_html=True)

    writeProvinceGraph(dfAdmin, dfDistr, 'BC')
    writeProvinceGraph(dfAdmin, dfDistr, 'Alberta')
    writeProvinceGraph(dfAdmin, dfDistr, 'Ontario')
    writeProvinceGraph(dfAdmin, dfDistr, 'Quebec')

def writeProvinceGraph(dfAdmin, dfDistr, province):
    dfAdmin = dfAdmin[dfAdmin['province'] == f'{province}']
    dfDistr = dfDistr[dfDistr['province'] == f'{province}']

    # ------------------------------------------------------------------------

    st.markdown('<hr style="border-top: 8px solid #ccc; border-radius: 5px;" />', unsafe_allow_html=True)

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title(f'{province} Vaccines', fontsize='large')
    plt.xlabel="Date"
    plt.ylabel="Number"

    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

    plt.bar(dfDistr['date_vaccine_distributed'], dfDistr['cumulative_dvaccine'], label=f'{province} Vaccines Distributed')
    plt.bar(dfAdmin['date_vaccine_administered'], dfAdmin['cumulative_avaccine'], label=f'{province} Vaccines Administered')
    plt.legend(['Distributed','Administered'])
    plt.grid(b=True, which='major')
    
    st.pyplot(fig1)
    plt.close()

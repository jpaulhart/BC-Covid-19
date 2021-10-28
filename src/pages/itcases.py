#!/usr/bin/env python3
#
# itcases.py
#
# bccases.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""itcases page shows regional Italy Covid Cases"""
import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from pandas.io.parsers import ParserBase
import streamlit as st
import awesome_streamlit as ast

import constants as cn

# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    st.title("Italian Regional Cases")
    cn.DATE_SPANS()
    
    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)

    regions = [
        "Lazio",      # 12
        "Puglia",     # 16
        "Sicilia",    # 19
        "Basilicata", # 17
        "Calabria",   # 18
        "Campania",   # 15
        "Sardegna",   # 20
        "Umbria"      # 19
    ] 

    df = pd.read_csv(cn.ITALY_DATA)
    df['data'] = df['data'].map(lambda x: x[0:10])

    regionCount = 0
    for region in regions:
        regionCount += 1
        dfRegion = df[df["denominazione_regione"] == region]
        dfRegion['nuovi_deceduti'] = dfRegion['deceduti'].diff(1)
        '''
        df['Rolling'] = df['Price'].rolling(5).mean()
        print(df.head(10))
        '''
 
        dfRegion = dfRegion.tail(40)
        dfRegion["rolling"] = dfRegion["nuovi_positivi"].rolling(10).mean()
        dfRegion = dfRegion.tail(30)
           
        dfFirst = dfRegion.head(1)
        firstDate = dfFirst["data"]
        cn.ITALY_FIRST_DATE = firstDate
        
        dfLast = dfRegion.tail(1)
        lastDate = dfLast["data"]
        cn.ITALY_LAST_DATE = lastDate

        fig1 = plt.figure(1, figsize=(8, 5))

        plt.title(f'{region} - New Cases and New Deaths', fontsize='large')
        plt.xlabel="Date"
        plt.ylabel="Number"

        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

        #plt.plot(dfPr['date'], dfProv['confirmedNewMean'], label='New Cases - Smoothed')
        #plt.plot(dfRegion['data'], dfRegion['totale_positivi'], label='Total Positives')
        plt.bar(dfRegion['data'], dfRegion['nuovi_positivi'], label='New Positives', color='0')
        plt.plot(dfRegion['data'], dfRegion['rolling'], label='Average New Positives', color='r')
        plt.plot(dfRegion['data'], dfRegion['nuovi_deceduti'], label='Deaths', color='c')
        #plt.plot(dfRegion['data'], dfRegion['totale_casi'], label='Total Cases')

        # Add a legend
        plt.legend(['Average New Positives', 'New Deaths', 'New Positives'])
        plt.grid(b=True, which='major')
        st.pyplot(fig1)
        #plt.show()
        plt.close()

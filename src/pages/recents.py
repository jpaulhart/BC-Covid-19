#!/usr/bin/env python3
#
# provinces.py
#
# provinces.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""countries page shows graphs about various countries cases"""
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
    """Used to write the page in the streamlit_app.py file"""
    st.title("Countries Covid Cases")
    cn.DATE_SPANS()
    st.markdown('#### ')

    country_lists = [
        ['Italy'], 
        ['Spain'], 
        ['Portugal'], 
        ['France'],
        ['Canada'],
        ['US'],
        ['Oman','Jordan','Morocco','Tunisia', 'Algeria'],
        ['Thailand','Cambodia','Vietnam'],
        ['Argentina','Chile','Uruguay'],
    ]        

    # Detail trend report for select countries
    for country_list in country_lists:
        print(f"Countries: {len(country_list)}, Country List: {country_list}")
        if len(country_list) != 1:
            return

        country_display = ', '.join(country_list)
        st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
        #st.markdown(f'**Country:** {country_display}')
        st.markdown('#### ')

        fig2 = plt.figure(1, figsize=(8, 5))

        plt.xlabel="Date"
        plt.ylabel="Number"

        #plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

        for cty in country_list:
            plt.title(f'{cty} New Confirmed Cases - Last 20 Days', fontsize='large')
            file_name = cty + '.csv'
            file_url = f'{cn.CASES_BASE_URL}{file_name.replace(" ", "%20")}'
            df = pd.read_csv(file_url)
            df = df.tail(20)
            plt.plot(df['Date'], df['ConfirmedNewMean'], label=df['Country_Region'], color = 'green')
            plt.bar(df['Date'], df['ConfirmedNew'], label=df['Country_Region'], color = 'lightseagreen')

        # Add a legend
        plt.legend(country_list)
        plt.grid(b=True, which='major')
        st.pyplot(fig2)
        plt.close()



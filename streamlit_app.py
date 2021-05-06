#!/usr/bin/env python3
#
# streamlit_app.py
#
# streamlit_app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

import datetime
from   datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import streamlit as st

import awesome_streamlit as ast
import constants as cn
import src.pages.about
import src.pages.bccases
import src.pages.countries
import src.pages.provinces
import src.pages.vaccinations

ast.core.services.other.set_logging_format()

PAGES = {
    "B.C. Cases": src.pages.bccases,
    "Vaccinations": src.pages.vaccinations,
    "Provinces": src.pages.provinces,
    "Countries": src.pages.countries,
    "About": src.pages.about,
}

# #######################################################################################
# Global Variables
# #######################################################################################

canada_url = f'{cn.CASES_BASE_URL}Canada.csv'
df = pd.read_csv(canada_url)
dfLast = df.tail(n=1)
cn.LAST_DATE = dfLast['Date'].values[0]
dfFirst = df.head(n=1)
cn.FIRST_DATE = dfFirst['Date'].values[0]
date_range = f'Data range: {cn.FIRST_DATE} to {cn.LAST_DATE}'

# Create dataframe with all records
dfCdc = pd.read_csv(cn.BC_REGIONAL_URL)
dfCdc = dfCdc.sort_values(by=['Date', 'HA', 'HSDA'], ascending=[True, True, True])
cn.BCCDC_FIRST_DATE = dfCdc.Date.values[0]
dfCdc = dfCdc.tail(n=1)
cn.BCCDC_LAST_DATE = dfCdc.Date.values[0]

dfAdmin = pd.read_csv(cn.CANADA_VACCINATION_ADMINSTERED)
dfAdmin['date_vaccine_administered64']= pd.to_datetime(dfAdmin['date_vaccine_administered'], format='%d-%m-%Y')
dfFirstDate = dfAdmin.head(n=1)
cn.VAX_FIRST_DATE = dfFirstDate['date_vaccine_administered64'].values[0]
cn.VAX_FIRST_DATE = np.datetime_as_string(cn.VAX_FIRST_DATE, unit='D') 
dfLastDate = dfAdmin.tail(n=1)
cn.VAX_LAST_DATE = dfLastDate['date_vaccine_administered64'].values[0]
cn.VAX_LAST_DATE = np.datetime_as_string(cn.VAX_LAST_DATE, unit='D')

# ############################################################################
# Entry Point
# ############################################################################

def main():
    """Main function of the App"""
    st.sidebar.subheader("COVID-19")
    #st.sidebar.markdown(f'<div style="font-size: 9pt">{date_range}</div>\n', unsafe_allow_html=True)
    
    st.sidebar.subheader("Navigation")
    selection = st.sidebar.radio("Select report to view:", list(PAGES.keys()))

    #print('--------------- Selection before')
    page = PAGES[selection]
    #print(f'--------------- Selection:', {page})

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.subheader("About")
    st.sidebar.info(
        """
        All data used in this app is provided by official sources:
        ### Data Sources
        1. Case data is from [CSSE at Johns Hopkins University COVID-19 Github repository]
        (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data).
        2. BC testing data for from the [BC Centre for Disease Control]
        (http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv)
        3. Canadian vaccination data is found in the [COVID-19 Canada Github repository]
        (https://github.com/ishaberry/Covid19Canada)
        """
    )


if __name__ == "__main__":
    main()

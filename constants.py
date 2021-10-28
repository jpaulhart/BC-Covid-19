#!/usr/bin/env python3
#
# constants.py
#
# app.py is a web application written in Python and using
# Streamlit as the presentation method.
#

# #######################################################################################
# Global Constants
# #######################################################################################

import streamlit as st

# Country files base url
# Field Names:
# Province_State, Country_Region, Lat, Long, Date, Confirmed, Deaths, Combined_Key, Population,
# ConfirmedNew, DeathsNew, ConfirmedNewMean, DeathsNewMean
# Country.csv fields
CASES_BASE_URL = 'https://raw.githubusercontent.com/jpaulhart/BC-Covid-19-Data/main/CSV_Files/'

# BC CDC testing data locations
# Field Names:
# "Date", "Region", "New_Tests", "Total_Tests", "Positivity", "Turn_Around"
#BC_TESTS_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.csv'
BC_TESTS_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Lab_Information.xlsx'

# "Reported_Date","HA","Sex","Age_Group","Classification_Reported"
BC_CASES_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv'
# "Date","Province","HA","HSDA","Cases_Reported","Cases_Reported_Smoothed"
BC_REGIONAL_URL = 'http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Regional_Summary_Data.csv'

# Canada Vaccination stats
# "date_vaccine_administered","province","cumulative_avaccine"
CANADA_VACCINATION_ADMINSTERED = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_administration_timeseries_prov.csv'
# "province","date_vaccine_completed","cvaccine","cumulative_cvaccine"
CANADA_VACCINATION_COMPLETED = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_completion_timeseries_prov.csv'
# "date_vaccine_distributed","province","cumulative_dvaccine"
CANADA_VACCINATION_DISTRIBUTED = 'https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/vaccine_distribution_timeseries_prov.csv'

COUNTRY_DATA = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

ITALY_DATA = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'

# Horizontal Rule
HORIZONTAL_RULE = '<hr style="border-top: 5px solid #F63366; border-radius: 5px;" />'

# combined_key,file_name,country,province
# Index.csv fields

# Provincial Population
PROV_POP = {
    'BC' : 5.071,
    'AL' : 4.371,
    'SA' : 1.174,
    'MB' : 1.369,
    'ON' : 14.57,
    'PQ' : 8.485,
    'NL' : 0.552,
    'NB' : 0.777,
    'NS' : 0.971,
    'PE' : 0.156,
}

FIRST_DATE = ""
LAST_DATE = ""

BCCDC_FIRST_DATE  = ""
BCCDC_LAST_DATE  = ""

VAX_FIRST_DATE  = ""
VAX_LAST_DATE  = ""

ITALY_FIRST_DATE  = ""
ITALY_LAST_DATE  = ""

def DATE_SPANS():
    #st.markdown(f'<div style="font-size: 9pt">Case Dates: {FIRST_DATE} to {LAST_DATE}</div>\n', unsafe_allow_html=True)
    #st.markdown(f'<div style="font-size: 9pt">BCCDC Dates: {BCCDC_FIRST_DATE} to {BCCDC_LAST_DATE}</div>\n', unsafe_allow_html=True)
    #st.markdown(f'<div style="font-size: 9pt">Vaccination Dates: {VAX_FIRST_DATE} to {VAX_LAST_DATE}</div>\n', unsafe_allow_html=True)
    table_rows =  '<div style="font-size: 9pt">\n'
    table_rows += '<table cellspacing=0 cellpadding=0 style="border:0px;">\n'
    table_rows += f'<tr><td>Case&nbsp;Data:<br />BCCDC&nbsp;Data:<br />BC&nbsp;Vaccination&nbsp;Data:&nbsp;Italy&nbsp;Data:<td width="100%">{FIRST_DATE} to {LAST_DATE}<br />{BCCDC_FIRST_DATE} to {BCCDC_LAST_DATE}<br/>{VAX_FIRST_DATE} to {VAX_LAST_DATE}<br/>{ITALY_FIRST_DATE} to {ITALY_LAST_DATE}</td></tr>'
    table_rows += '</table>\n'
    table_rows += '</div>\n'
    st.markdown(table_rows, unsafe_allow_html=True)
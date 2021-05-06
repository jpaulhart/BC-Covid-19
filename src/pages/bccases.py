#!/usr/bin/env python3
#
# bccases.py
#
# bccases.py is part of a web application written in Python and using
# Streamlit as the presentation method.
#

"""bccases page shows BC Covid Cases"""
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
    st.title("BC Covid Cases")
    cn.DATE_SPANS()
    
    prov = 'British Columbia'
    
    file_name = f'{prov}.csv'.replace(' ', '%20')
    print('Case file:', file_name)
    dfProv = pd.read_csv(f'{cn.CASES_BASE_URL}{file_name}')
    dfProv = fixBCCases(dfProv)
    dfProv = dfProv.replace(np.nan,0)
    #dfProv = dfProv.sort_values('Date', ascending=False)
    #print(dfProv)    
    
    # print('Test file:', cn.BC_TESTS_URL)
    # dfTests = pd.read_excel(cn.BC_TESTS_URL)
    # print('Test file:', cn.BC_TESTS_URL, 'loaded')
    # dfTests["Date"] = pd.to_datetime(dfTests["Date"]).dt.strftime('%Y-%m-%d')
    # #print(dfTests)
    # dfTable = dfTests.copy() 
    # dfTable['New_Positives'] = dfTable['New_Tests'] * (dfTable['Positivity'] / 100)

    # dfTable = dfTable.groupby('Date').agg({'New_Tests': 'sum', 'New_Positives': 'sum', 'Positivity': 'mean', 'Turn_Around': 'mean'})
    # dfTable = dfTable.sort_values('Date', ascending=False)
    # #print(dfTable)
    # print('Merging dataframes')
    # dfTable = pd.merge(dfProv, dfTable, on=['Date'], how='outer')
    # dfTable = dfTable.replace(np.nan,0)
    #print(dfTable)

    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
    casesByDate(dfProv)
    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
    casesByAge()
    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
    graphsByGraphs(dfProv)
    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
    casesByHA()
    #st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)
    #casesByHAGraph()

def fixBCCases(dfProv):
    zeroCount = 0
    zeroIndices = []
    for index, row in dfProv.iterrows():
        if row['Date'] >= '2020-07-01':
            if row['ConfirmedNew'] == 0:
                zeroCount += 1
                zeroIndices.append(index)
            elif zeroCount > 1:
                mondayCases = row['ConfirmedNew']
                eachDay = mondayCases // (zeroCount + 1)
                diff = mondayCases - (eachDay * (zeroCount + 1))
                #print(f"Zero count: {zeroCount}, Monday: {mondayCases}, Each day: {eachDay}, Diff: {diff}")
                #print(f"Indices: {zeroIndices}")
                dfProv.at[index, 'ConfirmedNew'] = eachDay + diff
                index = 0
                for i in zeroIndices:
                    #print("Index: {i}, {zeroIndices}")
                    dfProv.at[i, 'ConfirmedNew'] = eachDay
                    index += 1
                zeroCount = 0
                zeroIndices = []    
    
    dfProv['ConfirmedNewMean'] = dfProv['ConfirmedNew'].rolling(7).mean()

    return dfProv

#
#  Display Cases by date
#
def casesByDate(dfProv):
    st.markdown('#### BC New Cases and Deaths by Date')
    st.markdown('#### ')
    
    #st.markdown(f'##### 10 Days')

    # Table of details for last week 
    cases_data = '<div style="font-size: 9pt">\n'
    cases_data += '<table border=1>\n'
    cases_data += '<tr><th> </th><th colspan=2 style="text-align:center">Cases</th><th colspan=2 style="text-align:center">Deaths</th><th colspan=4 style="text-align:center">Testing</th></tr>\n'
    cases_data += '<tr><th>Date</th><th>Total</th><th>New</th><th>Total</th><th>New</th><th>New</th><th>Positives</th><th>% Pos.</th><th>Hours</th></tr>\n'
    #cases_data += '| :----- | ----------: | --------: | -----------: | ---------: |\n'
    row_count = 0
    dfSorted = dfProv.sort_values(['Date'], ascending=False)
    for index, row in dfSorted.iterrows():
        date = row['Date'] 
        confirmed = row['Confirmed']
        confirmed = "{:,}".format(confirmed)
        confirmedNew = row['ConfirmedNew']
        confirmedNew = "{:,}".format(confirmedNew)
        deaths = row['Deaths']
        deaths = "{:,}".format(deaths)
        deathsNew = row['DeathsNew']
        deathsNew = "{:,}".format(deathsNew)
        #New_Tests  New_Positives  Positivity  Turn_Around
        # newTests = row['New_Tests']
        # newTests = "{:,.0f}".format(newTests)
        # newPositives = row['New_Positives']
        # newPositives = "{:,.0f}".format(newPositives)
        # positivity = row['Positivity']
        # positivity = "{:.1f}".format(positivity)
        # turnAround = row['Turn_Around']
        # turnAround = "{:.1f}".format(turnAround)
        newTests = 0
        newTests = "{:,.0f}".format(newTests)
        newPositives = 0
        newPositives = "{:,.0f}".format(newPositives)
        positivity = 0
        positivity = "{:.1f}".format(positivity)
        turnAround = 0
        turnAround = "{:.1f}".format(turnAround)
        cases_data += f'<tr>'
        cases_data += f'<td nowrap>{date}</td><td style="text-align:right">{confirmed}</td>'
        cases_data += f'<td style="text-align:right">{confirmedNew}</td>'
        cases_data += f'<td style="text-align:right">{deaths}</td>'
        cases_data += f'<td style="text-align:right">{deathsNew}</td>'
        cases_data += f'<td style="text-align:right">{newTests}</td>'
        cases_data += f'<td style="text-align:right">{newPositives}</td>'
        cases_data += f'<td style="text-align:right">{positivity}%</td>'
        cases_data += f'<td style="text-align:right">{turnAround}</td>'
        cases_data += f'</tr>' + '\n'
        row_count += 1
        if row_count >= 10:
            cases_data += '</table>\n'
            cases_data += '</div>\n'
            break
    st.markdown(cases_data, unsafe_allow_html=True)

#
#  Display Cases on a graph
#
def graphsByGraphs(dfProv):    
    st.markdown('#### BC New Cases and Deaths by Date')
    st.markdown('#### ')

    #-------------------------------------------------------------------------
    # Create Confirmed New Plot
    #-------------------------------------------------------------------------
    #col1, col2 = st.beta_columns(2)
    #with col1:

    #st.markdown(f'##### New Cases')

    fig1 = plt.figure(1, figsize=(8, 5))

    plt.title('New Cases - Smoothed', fontsize='large')
    plt.xlabel="Date"
    plt.ylabel="Number"

    #plt.xticks(rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

    plt.plot(dfProv['Date'], dfProv['ConfirmedNewMean'], label='New Cases - Smoothed')
    plt.grid(b=True, which='major')
    
    st.pyplot(fig1)
    plt.close()

    #-------------------------------------------------------------------------
    # Create Deaths New Plot
    #-------------------------------------------------------------------------

    #with col2:
        
    fig2 = plt.figure(2, figsize=(8, 5))

    plt.title('New Deaths - Smoothed')
    plt.xlabel="Date"
    plt.ylabel="Number"

    #plt.xticks(rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))

    plt.plot(dfProv['Date'], dfProv['DeathsNewMean'], label='New Deaths - Smoothed')
    plt.grid(b=True, which='major')
    st.pyplot(fig2)
    plt.close()

#
#  Display Cases by Health Authority
#
def casesByHA():

    # Create dataframe with all records
    df = pd.read_csv(cn.BC_REGIONAL_URL)
    df = df.drop(columns=['Cases_Reported_Smoothed'])
    df = df.sort_values(by=['Date', 'HA', 'HSDA'], ascending=[False, True, True])

    # Create dataframe with records fromlast 7 days
    last_date = df.Date.values[0]
    first_date = (datetime.datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days = 7)).strftime('%Y-%m-%d')
    dfw = df[df['Date'] > first_date]

    # Group by HA and HSDA
    dfg = pd.DataFrame(df.groupby(['HA', 'HSDA'], as_index=False).sum())
    dfw = pd.DataFrame(dfw.groupby(['HA', 'HSDA'], as_index=False).sum())

    # Merge into a single dataframe
    df  = dfw.merge(dfg, left_on=['HA','HSDA'], right_on=['HA','HSDA'])
    table_rows =  '<div style="font-size: 9pt">\n'

    table_rows += '<table border=1 cellspacing=0 cellpadding=0>\n'
    table_rows += '<tr><th>Health Authority</th><th>Heath Services Delivery Area</th><th colspan=6 style="text-align:center">Cases</th></tr>\n'
    table_rows += '<tr><th></th><th></th><th colspan=3 style="text-align:center">Last 7 Days</th><th colspan=3 style="text-align:center">Cases Total</th></tr>\n'
    table_rows += '<tr><th></th><th></th><th style="text-align:center">Cases</th><th style="text-align:center">% of HA</th><th style="text-align:center">% of Tot</th><th style="text-align:center">Cases</th><th style="text-align:center">% of HA</th><th style="text-align:center">% of Tot</th></tr>\n'

    all_casex_total = 0
    all_casey_total = 0
    unique_has = df.HA.unique()
    for unique_ha in unique_has:
        dfha = df[df['HA'] == unique_ha]
        dfhagr =  pd.DataFrame(dfha.groupby(['HA', 'HSDA'], as_index=False).sum())
        ha = ''
        hsda = ''
        casex = ''
        casey = ''

        previous_ha = ''
        table_row = ''
        casex_total = 0
        casey_total = 0
        casex_percent = 0
        casey_percent = 0
        total_casex_percent = 0 
        total_casey_percent = 0 

        for index, row in dfhagr.iterrows():
            if row['HA'] != previous_ha:
                if previous_ha != '':
                    table_row = f'<tr valign="top"><td>{ha}</td><td nowrap>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casey}</td></tr>\n'
                    table_rows += table_row
                if row['HA'] == 'All':
                    all_casex_total = row['Cases_Reported_x']
                    all_casey_total = row['Cases_Reported_y']
                ha = f"<b>{row['HA']}</b>"

                hsda = f"<b>{row['HSDA']}</b>"
                casex = f"<b>{'{:,}'.format(row['Cases_Reported_x'])}</b>"
                casey = f"<b>{'{:,}'.format(row['Cases_Reported_y'])}</b>"
                casex_total = row['Cases_Reported_x']
                casey_total = row['Cases_Reported_y']
                cx = row['Cases_Reported_x']
                cpx = (cx / casex_total) * 100
                casex_percent = f"<b>" + '{:.2f}'.format(cpx) + '%</b>'
                total_casex_percent = f"<b>" + '{:.2f}'.format((row['Cases_Reported_x'] /  all_casex_total) * 100) + '%</b>'
                cy = row['Cases_Reported_y']
                cpy = (cy / casey_total) * 100
                casey_percent = f"<b>" + '{:.2f}'.format(cpy) + '%</b>'
                total_casey_percent = f"<b>" + '{:.2f}'.format((row['Cases_Reported_y'] /  all_casey_total) * 100) + '%</b>'
                previous_ha = row['HA']

            else:
                hsda += f"<br />{row['HSDA']}"
                casex += f"<br />{'{:,}'.format(row['Cases_Reported_x'])}"
                casey += f"<br />{'{:,}'.format(row['Cases_Reported_y'])}"
                casex_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_x'] /  casex_total) * 100) + '%'
                total_casex_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_x'] /  all_casex_total) * 100) + '%'
                casey_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_y'] /  casey_total) * 100) + '%'
                total_casey_percent += f"<br />" + '{:.2f}'.format((row['Cases_Reported_y'] /  all_casey_total) * 100) + '%'
        table_row = f'<tr valign="top"><td>{ha}</td><td nowrap>{hsda}</td><td style="text-align:right">{casex}</td><td style="text-align:right">{casex_percent}</td><td style="text-align:right">{total_casex_percent}</td><td style="text-align:right">{casey}</td><td style="text-align:right">{casey_percent}</td><td style="text-align:right">{total_casey_percent}</td></tr>\n'
        table_rows += table_row
    
    table_rows += '</table>\n'
    table_rows += '</div>\n'
    
    st.markdown('#### BCCDC Cases by Health Authority')
    st.markdown('#### ')
    st.markdown(table_rows, unsafe_allow_html=True)


#
#  Display Cases by Health Authority Graph
#
def casesByHAGraph():

    # Create dataframe with all records
    df = pd.read_csv(cn.BC_REGIONAL_URL)
    df = df[df['HA'] != 'Out of Canada']
    df = df[df['HSDA'] != 'All']
    df = df.drop(columns=['Cases_Reported_Smoothed', 'HSDA'])
    df = df.sort_values(by=['HA'], ascending=[True])
    # "Date","Province","HA","HSDA","Cases_Reported","Cases_Reported_Smoothed"
    dfgr =  pd.DataFrame(df.groupby(['HA'], as_index=False).sum())

    fig1 = plt.figure(1, figsize=(8, 8))

    plt.title('Cases by Health Authority - All Days', fontsize='large')

    explode = (0.1, 0.0, 0.2, 0.3, 0.0)
    colors = ( "orange", "cyan", "brown", 
            "grey", "indigo") 
    
    # Wedge properties 
    wp = { 'linewidth' : 1, 'edgecolor' : "green" } 

    # Creating autocpt arguments 
    def func(pct, allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return "{:.1f}%\n({:d} g)".format(pct, absolute) 
    
    unique_has = df.HA.unique()
    
    plt.pie(dfgr['Cases_Reported'], 
            autopct = lambda pct: func(pct, df['Cases_Reported']), 
            labels=unique_has,
            explode = explode) 

    st.pyplot(fig1)
    plt.close()

    st.markdown(cn.HORIZONTAL_RULE, unsafe_allow_html=True)

    # Create dataframe with all records
    df = pd.read_csv(cn.BC_REGIONAL_URL)
    df = df.sort_values(by=['Date', 'HA'], ascending=[False, True])

    last_date = df.Date.values[0]
    first_date = (datetime.datetime.strptime(last_date, '%Y-%m-%d') - timedelta(days = 7)).strftime('%Y-%m-%d')
    df = df[df['Date'] > first_date]
    df = df[df['HA'] != 'Out of Canada']
    df = df[df['HSDA'] != 'All']
    df = df.drop(columns=['Cases_Reported_Smoothed', 'HSDA'])
    df = df.sort_values(by=['HA'], ascending=[True])
    # "Date","Province","HA","HSDA","Cases_Reported","Cases_Reported_Smoothed"
    dfgr =  pd.DataFrame(df.groupby(['HA'], as_index=False).sum())

    fig1 = plt.figure(1, figsize=(8, 8))

    plt.title('Cases by Health Authority - Last Seven Days', fontsize='large')

    explode = (0.1, 0.0, 0.2, 0.3, 0.0)
    colors = ( "orange", "cyan", "brown", 
            "grey", "indigo") 
    
    # Wedge properties 
    wp = { 'linewidth' : 1, 'edgecolor' : "green" } 

    # Creating autocpt arguments 
    def func(pct, allvalues): 
        absolute = int(pct / 100.*np.sum(allvalues)) 
        return "{:.1f}%\n({:d} g)".format(pct, absolute) 
    
    unique_has = df.HA.unique()
    
    plt.pie(dfgr['Cases_Reported'], 
            autopct = lambda pct: func(pct, df['Cases_Reported']), 
            labels=unique_has,
            explode = explode) 

    st.pyplot(fig1)
    plt.close()


#
#  Display Cases by Health Age
#
def casesByAge():

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
    #plt.show()
    st.pyplot(fig1)
    plt.close()

# Create dataframe with all records
# df = pd.read_csv(cn.BC_CASES_URL)
# df = df.sort_values(by=['Reported_Date', 'HA', 'Age_Group'], ascending=[True, True, True])
# df = df.drop(columns=['Sex', 'Classification_Reported'])
# df = df.rename(columns={"HA": "Count"})

# last_date = df.tail(n=1)["Reported_Date"].values[0]
# dt = datetime.strptime(last_date, '%Y-%m-%d').date()

# dt7 = dt - timedelta(days = 7)
# last_week = dt7.strftime("%Y-%m-%d")
# df7 = df[df["Reported_Date"] > last_week]

# dt30 = dt - timedelta(days = 30)
# last_30 = dt30.strftime("%Y-%m-%d")
# df30 = df[df["Reported_Date"] > last_30]

# df7g = pd.DataFrame(df7.groupby(['Age_Group'], as_index=False).count())
# df30g = pd.DataFrame(df30.groupby(['Age_Group'], as_index=False).count())

# ax = df30g.plot.barh(x='Age_Group', y='Count')

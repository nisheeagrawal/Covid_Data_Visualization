#Nishee Agrawal
#Covid 19 Data Visualization Dashboard[Python,Plotly,Pandas]



import pandas as pd
import streamlit as st
from urllib.request import urlopen
import json
import plotly.express as px

covid_confirmed_data_file=r"D:\Nishee\covid_confirmed_usafacts.csv"
covid_deaths_data_file=r"D:\Nishee\covid_deaths_usafacts.csv"
covid_county_population_data_file=r"D:\Nishee\covid_county_population_usafacts.csv"


confirmed_cases_data = pd.read_csv(covid_confirmed_data_file, header=0)
confirmed_cases_data = confirmed_cases_data.set_index(['County Name', 'State', 'countyFIPS','StateFIPS']).stack().reset_index().rename(columns={'level_4':'date', 0:'count'})
confirmed_cases_data = confirmed_cases_data[confirmed_cases_data['countyFIPS']!=0][["countyFIPS","date","count"]]
confirmed_cases_data['date']=pd.to_datetime(confirmed_cases_data['date'], format='%Y-%m-%d')
confirmed_cases_data['Confirmed Count'] = confirmed_cases_data.sort_values(by=['date'], ascending=True).groupby(['countyFIPS'])['count'].diff()
confirmed_cases_filter_data = confirmed_cases_data.groupby(['countyFIPS',pd.Grouper(key='date', freq='W-SUN')]).filter(lambda x: len(x) == 7)
st.line_chart(confirmed_cases_filter_data.groupby([pd.Grouper(key='date', freq='W-SUN')])['Confirmed Count'].sum().reset_index().set_index('date'))


death_cases_data = pd.read_csv(covid_deaths_data_file, header=0)
death_cases_data = death_cases_data.set_index(['County Name', 'State', 'countyFIPS','StateFIPS']).stack().reset_index().rename(columns={'level_4':'date', 0:'count'})
death_cases_data = death_cases_data[death_cases_data['countyFIPS']!=0][["countyFIPS","date","count"]]
death_cases_data['date']=pd.to_datetime(death_cases_data['date'], format='%Y-%m-%d')
death_cases_data['Death Count'] = death_cases_data.sort_values(by=['date'], ascending=True).groupby(['countyFIPS'])['count'].diff()
death_cases_data_filter_data = death_cases_data.groupby(['countyFIPS',pd.Grouper(key='date', freq='W-SUN')]).filter(lambda x: len(x) == 7)
st.line_chart(death_cases_data_filter_data.groupby([pd.Grouper(key='date', freq='W-SUN')])['Death Count'].sum().reset_index().set_index('date'))

covid_county_population = pd.read_csv(covid_county_population_data_file)

confirmed_cases_filter_group_data = confirmed_cases_filter_data.groupby(['countyFIPS',pd.Grouper(key='date', freq='W-SUN')])['Confirmed Count'].sum().reset_index()
confirmed_cases_filter_group_data = pd.merge(confirmed_cases_filter_group_data, covid_county_population, on="countyFIPS", how='left')
confirmed_cases_filter_group_data['Confirmed Count'] = (confirmed_cases_filter_group_data['Confirmed Count'].astype(int) * 100000) / confirmed_cases_filter_group_data['population']
confirmed_cases_filter_group_data['countyFIPS'] = confirmed_cases_filter_group_data['countyFIPS'].astype(str).apply(lambda x: x.zfill(5))
confirmed_cases_filter_group_data['date'] = confirmed_cases_filter_group_data.date.apply(lambda x: x.date()).apply(str)


death_cases_filter_group_data = death_cases_data_filter_data.groupby(['countyFIPS',pd.Grouper(key='date', freq='W-SUN')])['Death Count'].sum().reset_index()
death_cases_filter_group_data = pd.merge(death_cases_filter_group_data, covid_county_population, on="countyFIPS", how='left')
death_cases_filter_group_data['Death Count'] = (death_cases_filter_group_data['Death Count'].astype(int) * 100000) / death_cases_filter_group_data['population']
death_cases_filter_group_data['countyFIPS'] = death_cases_filter_group_data['countyFIPS'].astype(str).apply(lambda x: x.zfill(5))
death_cases_filter_group_data['date'] = death_cases_filter_group_data.date.apply(lambda x: x.date()).apply(str)

sl_date = st.select_slider(
     'Choose a week in the slider - Question 3, 4 and 5',
     options=confirmed_cases_filter_group_data['date'].unique().tolist())

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

st.write(px.choropleth(confirmed_cases_filter_group_data[confirmed_cases_filter_group_data['date']==sl_date], geojson=counties, locations='countyFIPS', color='Confirmed Count',
                            color_continuous_scale="twilight",
                            scope="usa",
                            width=900,
                            height=500,
                            title = "New Confirmed Cases Countywise Weekly " + sl_date
                           ))
st.write(px.choropleth(death_cases_filter_group_data[death_cases_filter_group_data['date']==sl_date], geojson=counties, locations='countyFIPS', color='Death Count',
                            color_continuous_scale="twilight",
                            scope="usa",
                            width=900,
                            height=500,
                            title = "Death Cases Countywise Weekly " + sl_date
                           ))

if st.button('Run Animatinon - Question 6'):
    confirmed_spot = st.empty()
    death_spot = st.empty()
    for date in confirmed_cases_filter_group_data['date'].unique().tolist():
        with confirmed_spot:
            st.write(px.choropleth(confirmed_cases_filter_group_data[confirmed_cases_filter_group_data['date']==date], geojson=counties, locations='countyFIPS', color='Confirmed Count',
                            color_continuous_scale="twilight",
                            scope="usa",
                            width=900,
                            height=500,
                            title = "New Confirmed Cases Countywise Weekly " + date
                           ))
        with death_spot:
            st.write(px.choropleth(death_cases_filter_group_data[death_cases_filter_group_data['date']==date], geojson=counties, locations='countyFIPS', color='Death Count',
                            color_continuous_scale="twilight",
                            scope="usa",
                            width=900,
                            height=500,
                            title = "Death Cases Countywise Weekly " + date
                           ))

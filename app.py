import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt

india_df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
state_df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
state_cu = pd.read_csv('https://api.covid19india.org/csv/latest/states.csv')
district_data = pd.read_csv('https://api.covid19india.org/csv/latest/districts.csv')
district_data.replace('Unknown', 'Other', inplace=True)
df = gpd.read_file('india_administrative_state_boundary.shp')
state_data = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
state_data = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')

state_data.drop(labels=[0, 31, 18], inplace=True)
df.drop(labels=7, inplace=True)
df = df.rename(columns={'st_nm':'State'})
df = df[['State', 'geometry']]
df = df.replace('Dadara & Nagar Havelli', 'Dadra and Nagar Haveli and Daman and Diu')
df = df.replace('NCT of Delhi', 'Delhi')
df = df.replace('Jammu & Kashmir', 'Jammu and Kashmir')
df = df.replace('Arunanchal Pradesh', 'Arunachal Pradesh')
df = df.replace('Andaman & Nicobar Island', 'Andaman and Nicobar Islands')
merged = df.merge(state_data, how='left')

state_codes = {'Andaman and Nicobar Islands': 'AN',
 'Andhra Pradesh': 'AP',
 'Arunachal Pradesh': 'AR',
 'Assam': 'AS',
 'Bihar': 'BR',
 'Chandigarh': 'CH',
 'Chhattisgarh': 'CT',
 'Dadra and Nagar Haveli and Daman and Diu': 'DN',
 'Delhi': 'DL',
 'Goa': 'GA',
 'Gujarat': 'GJ',
 'Haryana': 'HR',
 'Himachal Pradesh': 'HP',
 'Jammu and Kashmir': 'JK',
 'Jharkhand': 'JH',
 'Karnataka': 'KA',
 'Kerala': 'KL',
 'Ladakh': 'LA',
 'Lakshadweep': 'LD',
 'Madhya Pradesh': 'MP',
 'Maharashtra': 'MH',
 'Manipur': 'MN',
 'Meghalaya': 'ML',
 'Mizoram': 'MZ',
 'Nagaland': 'NL',
 'Odisha': 'OR',
 'Puducherry': 'PY',
 'Punjab': 'PB',
 'Rajasthan': 'RJ',
 'Sikkim': 'SK',
 'Tamil Nadu': 'TN',
 'Telangana': 'TG',
 'Tripura': 'TR',
 'Uttar Pradesh': 'UP',
 'Uttarakhand': 'UT',
 'West Bengal': 'WB'}

st.title('COVID-19 in India')
st.markdown('The following is an analysis and visualization of the COVID-19 pandemic in India. You can view active cases, confirmed cases, recoveries and deaths. The data can be viewed countrywise, state-wise and even district-wise. Scroll down to view state-wise and district-wise data. The APIs and resources used for this project can be found [here](https://api.covid19india.org/).')
st.markdown('All the visualizations are interactive.')

def create_plot(x, y, labels):
    fig = px.line(x=x, y=y, labels=labels)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(showgrid=False)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig, use_container_width=True)

def country_plots():
    st.subheader('Confirmed cases in India')
    create_plot(x=india_df['Date_YMD'], y=india_df['Total Confirmed'], labels={'x':'Time', 'y':'Confirmed cases'})
    
    st.subheader('Recoveries in India')
    create_plot(x=india_df['Date_YMD'], y=india_df['Total Recovered'], labels={'x':'Time', 'y':'Recoveries'})

    st.subheader('Deaths in India')
    create_plot(x=india_df['Date_YMD'], y=india_df['Total Deceased'], labels={'x':'Time', 'y':'Deaths'})
    
    st.subheader('Active cases in India')
    create_plot(x=india_df['Date_YMD'], y=india_df['Total Confirmed']-india_df['Total Recovered']-india_df['Total Deceased'], labels={'x':'Time', 'y':'Active cases'})
 
with st.beta_container():

    variable = st.selectbox('Select map mode', ('Confirmed', 'Recovered', 'Deaths', 'Active'))
    variable_color = {'Confirmed': 'Reds', 'Recovered': 'Greens', 'Deaths': 'Greys', 'Active': 'Blues'}
    plt.style.use("dark_background")
    fig, ax = plt.subplots(1)
    fig.patch.set_alpha(0)
    ax.axis('off')
    vmin, vmax = 0, 10000000
    ax.set_title('{} cases'.format(variable))
    sm = plt.cm.ScalarMappable(cmap=variable_color[variable], norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    fig.colorbar(sm)
    merged.plot(column=variable, cmap=variable_color[variable], linewidth=0.8, ax=ax, edgecolor='0.2')
    st.pyplot(fig, use_container_width=True)

    country_plots()

    st.subheader("View data by state")
    state = st.selectbox('Select state', tuple(state_codes.keys()))
    mode = st.selectbox('Select mode', ('Cumulative', 'Daily'))
    
    if mode == 'Cumulative':
        st.subheader('Confirmed cases in {}'.format(state))
        create_plot(x=state_cu[state_cu['State'] == state]['Date'], y=state_cu[state_cu['State'] == state]['Confirmed'], labels={'x': 'Time', 'y': 'Confirmed'})

        st.subheader('Recoveries in {}'.format(state))
        create_plot(x=state_cu[state_cu['State'] == state]['Date'], y=state_cu[state_cu['State'] == state]['Recovered'], labels={'x': 'Time', 'y': 'Recoveries'})

        st.subheader('Deaths in {}'.format(state))
        create_plot(x=state_cu[state_cu['State'] == state]['Date'], y=state_cu[state_cu['State'] == state]['Deceased'], labels={'x': 'Time', 'y': 'Deaths'})
    
        st.subheader('Active cases in  {}'.format(state))
        create_plot(x=state_cu[state_cu['State'] == state]['Date'], y=state_cu[state_cu['State'] == state]['Confirmed'] - state_cu[state_cu['State'] == state]['Recovered'] - state_cu[state_cu['State'] == state]['Deceased'] - state_cu[state_cu['State'] == state]['Other'], labels={'x': 'Time', 'y':'Active cases'})
    
    if mode == 'Daily':
        st.subheader('Daily Confirmed cases in {}'.format(state))
        create_plot(x=state_df[state_df['Status'] == 'Confirmed']['Date_YMD'], y=state_df[state_df['Status'] == 'Confirmed'][state_codes[state]], labels={'x':'Time', 'y':'Daily confirmed cases'})

        st.subheader('Daily Recoveries in {}'.format(state))
        create_plot(x=state_df[state_df['Status'] == 'Recovered']['Date_YMD'], y=state_df[state_df['Status'] == 'Recovered'][state_codes[state]], labels={'x':'Time', 'y':'Daily recovered cases'})

        st.subheader('Daily Deaths in {}'.format(state))
        create_plot(x=state_df[state_df['Status'] == 'Deceased']['Date_YMD'], y=state_df[state_df['Status'] == 'Deceased'][state_codes[state]], labels={'x':'Time', 'y':'Daily deaths'})

        st.subheader('Daily Active cases in {}'.format(state))
        active = state_df[state_df['Status'] == 'Confirmed'][state_codes[state]].reset_index() - state_df[state_df['Status'] =='Recovered'][state_codes[state]].reset_index() - state_df[state_df['Status'] =='Deceased'][state_codes[state]].reset_index()
        create_plot(x=state_df[state_df['Status'] == 'Confirmed']['Date_YMD'], y=active[state_codes[state]], labels={'x':'Time', 'y':'Daily Active cases'})

    df = state_cu[state_cu['State'] == state]['Confirmed'] - state_cu[state_cu['State'] == state]['Recovered'] - state_cu[state_cu['State'] == state]['Deceased'] - state_cu[state_cu['State'] == state]['Other']
    st.text('Active ratio for {} is {:0.2f}%'.format(state, df.iloc[-1] / state_cu[state_cu['State'] == state]['Confirmed'].iloc[-1] * 100))
    st.text('Recovery ratio for {} is {:0.2f}%'.format(state, state_cu[state_cu['State'] == state]['Recovered'].iloc[-1] / state_cu[state_cu['State'] == state]['Confirmed'].iloc[-1]*100))
    st.text('Death ratio for {} is {:0.2f}%'.format(state, state_cu[state_cu['State'] == state]['Deceased'].iloc[-1] / state_cu[state_cu['State'] == state]['Confirmed'].iloc[-1]*100))

    st.subheader("View data by district")
    district = st.selectbox('Select district', district_data[district_data['State'] == state]['District'].unique())
     
    st.subheader('Confirmed cases in {}'.format(district))
    create_plot(x=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Date'],
        y=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Confirmed'],
        labels={'x': 'Time', 'y': 'Confirmed'})

    st.subheader('Recoveries in {}'.format(district))
    create_plot(x=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Date'],
        y=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Recovered'],
        labels={'x': 'Time', 'y': 'Recoveries'})

    st.subheader('Deaths in {}'.format(district))
    create_plot(x=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Date'],
        y=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Deceased'],
        labels={'x': 'Time', 'y': 'Recoveries'})

    st.subheader('Active cases in {}'.format(district))
    create_plot(x=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Date'],
        y=district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Confirmed']-district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Recovered']-district_data[(district_data['State'] == state) & (district_data['District'] == district)]['Deceased'],
        labels={'x': 'Time', 'y': 'Recoveries'})

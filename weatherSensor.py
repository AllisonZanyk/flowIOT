from time import sleep
import math
import pandas as pd
import streamlit as st 
from beebotte import *
import plotly.express as px # interactive charts

# Set the keys from my channel 
API_KEY = "R01VXaOherdFcEOhk1d1bt3B"
SECRET_KEY = "79R8swda1EBvqVajZZURSOxRbzQQgsgV" 

# Connect with my channel
bclient = BBT(API_KEY, SECRET_KEY)
channel = bclient.getChannel('humidity')

## Create a Resource object
humidity_resource = Resource(bclient, 'humidity', 'Humidity')
temp_resource = Resource(bclient, 'humidity', 'Temp')



# make a data frame
df = pd.DataFrame(
    [[0,0]], 
    columns=['temp', 'humidity']
    )

# Make the page
st.set_page_config(
    page_title='Dashboard: Temp and Humidity',
    page_icon='✅',
    layout='wide'
)

placeholder = st.empty()
placeholder2 = st.empty()

while True:
# read data
    NewHumidity = humidity_resource.read(limit = 1)
    NewHumidity = NewHumidity[0]['data']
    NewTemp = temp_resource.read(limit = 1)
    NewTemp = NewTemp[0]['data']

    with placeholder.container():
        newdf = pd.DataFrame([[NewHumidity, NewTemp]], 
            columns=['temp', 'humidity']
        )
        df = pd.concat([df,newdf],axis=0)
        sleep(1)
        # Display this in streamlit
        st.dataframe(df[-10:])

    with placeholder2.container():
        # split the dashboard here in 3 columns
        kpi1, kpi2 = st.columns(2)
        # fill in those three columns with respective metrics 
        # or KPIs (key performance indicators)
        kpi1.metric(
            label="Temp ",
            value=int(NewTemp),
            delta=(NewTemp) - 10, # delta allows to show a progression in the displayed value
        )

        kpi2.metric(
            label="Humidity",
            value=int(NewHumidity),
            delta=-10 + NewHumidity,
        )


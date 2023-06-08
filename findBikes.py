import streamlit as st
import numpy as np
import pandas as pd
import time # to simulate real time data
import plotly.express as px # interactive charts
import GetBikeData as gb
import haversine as hs
from decimal import Decimal, ROUND_HALF_UP

bikeCSV = gb.GetBikeData()
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv('BikeStations.csv')
df = get_data()

st.title("Find Bikes Dashboard")

currentlong = st.number_input('Insert your latitude: ')
currentlat = st.number_input('Insert your current longitude: ')

def bikeDistance(stationLong, stationLat, currentlong, currentlat):
    currentCoords = (currentlong, currentlat)
    desiredCoords = (stationLong, stationLat)
    distance = hs.haversine(currentCoords, desiredCoords)
    return distance

st.markdown("## Nearest Bikes")
# filter the distances based on this choice
distances = {}
for index, row in df.iterrows():
    distances[df["Street"][index]] = bikeDistance(row["longitude"], row["latitude"],currentlong, currentlat)


closest = (distances[df["Street"][0]], df["Street"][0])
for index, row in df.iterrows():
    current = distances[df["Street"][index]]
    if current < closest[0]:
        closest = (current, df["Street"][index])


st.write("The closest station: " , closest)
st.write('Your current coordinates are: ' + str(currentlong) + ' , ' + str(currentlat))
st.dataframe(df[0:5])
currentCoords = pd.DataFrame(data={'latitude': [currentlat], 'longitude': [currentlong]})
df = pd.concat([df , currentCoords])

worldmap = st.map(df)

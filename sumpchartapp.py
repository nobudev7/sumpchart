import streamlit as st
import requests
import pandas as pd
import datetime
import altair as alt


# Obtain the latest date of the data
url = 'http://localhost:8080/devices/1/entries/'
response = requests.get(url)
if response.status_code != 200:
    st.write('Response code: ' + str(response.status_code))
    raise SystemExit

entry = response.json()
dt = datetime.datetime.fromisoformat(entry.get("measuredOn"))

st.header("Sump Pump Data")

response = requests.get(url + dt.strftime('%Y/%m/%d'))
if response.status_code != 200:
    st.write('Response code: ' + str(response.status_code))
    raise SystemExit

entries_json = response.json()
entries_df = pd.DataFrame(entries_json)
#st.line_chart(entries_df, x='measuredOn', y='value')

entries_df['time'] = pd.to_datetime(entries_df['measuredOn']).dt.strftime("%H:%M:%S")
entries_df['waterlevel'] = entries_df['value'].div(10)
#st.write(entries_df)

chart = (
        alt.Chart(
            data=entries_df,
            title="Water Level on " + dt.strftime('%Y/%m/%d'),
        )
        .mark_line()
        .encode(
            x=alt.X("time", axis=alt.Axis(title="Time")),
            y=alt.Y("waterlevel", axis=alt.Axis(title="Water Level (cm)")),
        )
)

st.altair_chart(chart, use_container_width=True)




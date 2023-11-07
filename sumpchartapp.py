import streamlit as st
import requests
import pandas as pd
import datetime
import altair as alt


base_url = 'http://localhost:8080/devices/1/entries'

# Obtain the latest date of the data
response = requests.get(base_url)
if response.status_code != 200:
    st.write('URL: ' + base_url)
    st.write('Response code: ' + str(response.status_code))
    raise SystemExit

entry = response.json()
latest_dt = datetime.datetime.fromisoformat(entry.get("measuredOn"))

# Get oldest entry to set the min date for date picker
response = requests.get(base_url + "?ascending=true")
if response.status_code != 200:
    st.write('URL: ' + base_url)
    st.write('Response code: ' + str(response.status_code))
    raise SystemExit

entry = response.json()
oldest_dt = datetime.datetime.fromisoformat(entry.get("measuredOn"))

st.header("Sump Pump Data")
entries_df = pd.DataFrame()
chart_title = ""
st.sidebar.caption = chart_title

def update_data():
    global entries_df
    global chart_title
    query_date = selected_date.strftime("%Y/%m/%d")
    response = requests.get(base_url + "/" + query_date)
    if response.status_code != 200:
        st.write('URL: ' + base_url + "/" + query_date)
        st.write('Response code: ' + str(response.status_code))
        return

    entries_json = response.json()
    if len(entries_json) > 0:
        entries_df = pd.DataFrame(entries_json)

        entries_df['time'] = pd.to_datetime(entries_df['measuredOn']).dt.strftime("%H:%M:%S")
        entries_df['waterlevel'] = entries_df['value'].div(10)
        chart_title = "Water Level on "
    else:
        chart_title = "No data on "
        entries_df = pd.DataFrame([], columns=['time', 'waterlevel'])
    #st.write(entries_df)

selected_date = st.sidebar.date_input(label = "Select",
                                      value = latest_dt,
                                      on_change=update_data,
                                      min_value=oldest_dt,
                                      max_value=latest_dt
                                      )

update_data()

# st.line_chart(entries_df, x='measuredOn', y='value')

chart = (
        alt.Chart(
            data=entries_df,
            title = chart_title + selected_date.strftime("%Y/%m/%d"),
        )
        .mark_line()
        .encode(
            x=alt.X("time", axis=alt.Axis(title="Time")),
            y=alt.Y("waterlevel", axis=alt.Axis(title="Water Level (cm)")),
        )
)

st.altair_chart(chart, use_container_width=True)




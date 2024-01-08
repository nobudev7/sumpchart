import streamlit as st
import requests
import pandas as pd
import altair as alt

entry_url = 'http://localhost/devices/1/entries/'


def update_chart(date):
    entries_json = get_json_response(entry_url + date)

    if len(entries_json) > 0:
        entries_df = pd.DataFrame(entries_json)

        entries_df['time'] = pd.to_datetime(entries_df['measuredOn']).dt.strftime("%H:%M:%S")
        entries_df['waterlevel'] = entries_df['value'].div(10)
        chart_title = "Device 1 Water Level on "
    else:
        chart_title = "No data on "
        entries_df = pd.DataFrame([], columns=['time', 'waterlevel'])
    #st.write(entries_df)    
        
    chart = (
        alt.Chart(
            data=entries_df,
            title = chart_title + date,
        )
        .mark_line()
        .encode(
            x=alt.X("time", axis=alt.Axis(title="Time")),
            y=alt.Y("waterlevel", axis=alt.Axis(title="Water Level (cm)")),
        )
    )
    st.altair_chart(chart, use_container_width=True)

def get_json_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.write("Error in getting response: url=" + url)
        st.write('Response code: ' + str(response.status_code))
        return []


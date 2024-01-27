import streamlit as st
import requests
import pandas as pd
import altair as alt

entry_url = 'http://localhost:8080/devices/1/entries/'

def update_chart(date):
    max_y = 20
    note = ""
    entries_json = get_json_response(entry_url + date)

    if len(entries_json) > 0:
        entries_df = pd.DataFrame(entries_json)

        entries_df['time'] = pd.to_datetime(entries_df['measuredOn']).dt.strftime("%H:%M:%S")
        entries_df['waterlevel'] = entries_df['value'].div(10)
        max_level = entries_df['waterlevel'].max()
        if (max_level > 50):
            max_y = max_level
            note = "Note: Water level data contains abnormally high value"
        chart_title = "Device 1 Water Level on "
    else:
        chart_title = "No data on "
        entries_df = pd.DataFrame([], columns=['time', 'waterlevel'])
    # st.write(entries_df)    

    st.subheader(chart_title + date)
    if (note != ""):
        st.text(note)

    chart = (
        alt.Chart(
            data=entries_df,
        )
        .mark_line()
        .encode(
            x=alt.X("time", axis=alt.Axis(title="Time")),
            y=alt.Y("waterlevel", axis=alt.Axis(title="Water Level (cm)"), scale=alt.Scale(domain=[5, max_y])),
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


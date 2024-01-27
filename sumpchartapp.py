import streamlit as st
import pandas as pd
import datetime
import altair as alt
import utils


list_url = 'http://localhost:8080/devices/1/list'

st.header("Sump Water Level")
entries_df = pd.DataFrame()
chart_title = ""
st.sidebar.caption = chart_title

if 'years' not in st.session_state:
    years = utils.get_json_response(list_url)
    years.sort(reverse=True);
    st.session_state.years = years

yearmonthdict = {}
selected_month = ""
first_day_range = ""
last_day_range = ""
format = '%Y/%m/%d'

for year in st.session_state.years:
    st.sidebar.markdown('## ' + year)
    if "monthdatafor" + year not in st.session_state:
        month_url = list_url + "/" + year
        months = utils.get_json_response(month_url)
        months.sort(reverse=True)
        st.session_state["monthdatafor"+year] = months

    yearmonthdict[year] = st.session_state["monthdatafor"+year]
    for month in st.session_state["monthdatafor"+year]:
        if(st.sidebar.button(month)):
            selected_month = month

if selected_month == "":
    selected_month = yearmonthdict[st.session_state.years[0]][0]

# DEBUG st.write("selected_month:" + selected_month)

days = utils.get_json_response(list_url + "/" + selected_month)
days.sort(reverse=True)

for day in days:
    utils.update_chart(day)

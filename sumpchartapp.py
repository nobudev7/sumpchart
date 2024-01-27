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
latestmonth = ""
first_day_range = ""
last_day_range = ""
format = '%Y/%m/%d'

def date_selected():
    st.write("selected = " + st.session_state.selected_date.strftime("%Y/%m/%d"))

for year in st.session_state.years:
    st.sidebar.markdown('## ' + year)
    if "monthdatafor" + year not in st.session_state:
        month_url = list_url + "/" + year
        months = utils.get_json_response(month_url)
        months.sort(reverse=True)
        st.session_state["monthdatafor"+year] = months

    yearmonthdict[year] = st.session_state["monthdatafor"+year]
    for month in st.session_state["monthdatafor"+year]:
        selected_month = st.sidebar.button(month)
        if selected_month:
            #Debug st.sidebar.write("Selected Month: " + month)
            latestmonth = month
            days = utils.get_json_response(list_url + "/" + latestmonth)
            first_day_range = days[0]
            last_day_range = days[-1]
            #Debug st.sidebar.write(days)
            selected_date = st.sidebar.date_input(label = "Select",
                                      value = datetime.datetime.strptime(last_day_range,format),
                                      #Debug on_change=date_selected,
                                      key="selected_date",
                                      min_value=datetime.datetime.strptime(first_day_range,format),
                                      max_value=datetime.datetime.strptime(last_day_range,format)
                                      )

if latestmonth == "":
    latestmonth = yearmonthdict[st.session_state.years[0]][0]

if 'selected_date' not in st.session_state:
    days = utils.get_json_response(list_url + "/" + latestmonth)
    last_date = days[-1]
    #Debug st.write("last_date: " + last_date)
    st.session_state['selected_date'] = datetime.datetime.strptime(last_date, '%Y/%m/%d').date()


chart_day = st.session_state['selected_date'].strftime("%Y/%m/%d")
utils.update_chart(chart_day)

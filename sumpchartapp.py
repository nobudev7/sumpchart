import streamlit as st
import requests
import pandas as pd

st.title('Sump Pump Data')

url = 'http://192.168.1.169:8080/rest/all'
response = requests.get(url)
if response.status_code == 200:
    json_data = response.json()
    df = pd.DataFrame(json_data)
    st.line_chart(df, x='measuredOn', y='value')
else:
    st.write('Response code: ' + str(response.status_code))

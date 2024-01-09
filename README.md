# sumpchart
[![MIT Licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ntamagawa/sumpdata/blob/main/LICENSE)

This is a visualization web app for sump water level data managed by [Sump Water Level Application](https://github.com/ntamagawa/sumpdata) server. It is intended to be light and simple, just to showcase what the sump data (server) application can do.

![Web Frontend Sample](assets/WebFrontendSample.png)

## Environments
This web application is based on streamlit.
- Python 3
- streamlit (tested 1.28)
- pandas (tested 2.1)

## Streamlit Installation
``` bash
(venv) $ pip install streamlit
```
Detailed installation steps can be found in [Installing Streamlit on Mac](https://dev.to/developernt/streamlit-memo-cc1).

## Run
``` bash
(venv) $ streamlit run sumpchartapp.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.169:8501

```

## Features
- Visualize sump water level for a specified day
- Calendar widget let users to choose the day
- Handles the day when no data is available

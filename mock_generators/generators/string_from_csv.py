import pandas as pd
import io
import requests
import random
import logging
# Using streamlit's cache to avoid reloading the csv each time
import streamlit as st

@st.cache_data(ttl=60) # 1 minute
def csv_data(url: str):
    csv=requests.get(url).content
    df=pd.read_csv(io.StringIO(csv.decode('utf-8')))
    records = df.to_dict('records')
    return records

def generate(args: list[any]):
    url = args[0]
    field = args[1]
    try:
        data = csv_data(url)
        # Return a random item from list
        entry = random.choice(data)
        value = entry.get(field, None)
        return value
    except Exception as e:
        logging.error(f'Exception: {e}')
        return None

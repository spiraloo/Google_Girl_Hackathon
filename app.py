
# importing libraries
import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
import matplotlib.pyplot as plt

def read_data_set(file_name):
    df = pd.read_csv(file_name)
    return df

def load_data_set():
    df = read_data_set("Groceries_dataset.csv")
    return df

def process_data(df,item):
    # sort df by date and drop unused columns
    df = df.drop(columns=['Member_number'], axis=1)
   
    # get items with many data points
    valid_items_df = df.groupby(by="itemDescription").count().sort_values(by="Date")
    valid_items_df = valid_items_df.drop(valid_items_df[valid_items_df.Date < 5000].index)
    temp_df = df[df.itemDescription == item] # get df for each item
    temp_df["Date"] = pd.to_datetime(temp_df["Date"],dayfirst=True) # change date to datetime format
    temp_df = temp_df.sort_values(by="Date") # sort by date
    temp_df = temp_df.groupby(temp_df["Date"]).count() # groupby date and see frequency per date


    # forecast item using forecast function implemented
    pred = forecast(temp_df, item)
    save_forecast(pred, item)
    return pred

def forecast(my_data, food_label):
    from statsmodels.tsa.arima.model import ARIMA

    # ARIMA MODEL after considering
    # p (order of autoregressive model)
    # d (degree of differencing)
    # q (order of moving-average model)
    model = ARIMA(my_data, order=(7, 0, 7))
    results_ARIMA = model.fit()

    # forecast results
    x = results_ARIMA.forecast(steps=30)
    x.index = np.arange(1, len(x.index) + 1)
    return x

def save_forecast(forecast, label):
    data = [pred for pred in forecast.values]
import streamlit as st
df = load_data_set()
item = st.selectbox(
    'Food Item',
    ("bottled water", "other vegetables", "root vegetables", "sausage", "tropical fruit", "whole milk", "yogurt"))
pred=process_data(df,item)
st.line_chart(data=pd.DataFrame(pred))

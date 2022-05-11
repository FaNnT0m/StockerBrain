import streamlit as st
import pandas as pd
from PIL import Image
import yfinance as yf

import plotly.graph_objects as go

#import yfinance
st.set_page_config(layout="wide")
st.write("""


""")

st.sidebar.header('StockerBrain')

def get_input():#This functions take the user data
    stock_symbol = st.sidebar.text_input("Stock Symbol", "tcs.ns")
    s_date = st.sidebar.text_input("Start Date", "2020-01-01")
    e_date = st.sidebar.text_input("End Date", "2022-05-11")
    return s_date,e_date,stock_symbol.upper()



#get user input
startDate, endDate, symbol, =get_input()

#getting the data
#df = get_data(symbol, startDate, endDate)
df = yf.download(tickers = symbol, start = startDate , end=endDate, interval="1d")

#Adjusting data
df["DateTime"] = list(df.index)
df = df.reset_index(drop=True)

#Candlestick
fig = go.Figure(data=[go.Candlestick(x=df['DateTime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
fig.update_layout(yaxis_title = symbol.removesuffix('.NS')+" Price", xaxis_title = "Date", template ="plotly_dark")
fig.update_layout(autosize=False,width=1100,height=750,)

#fig.set_facecolor("#2596be")

# colorscale=["rgb(37, 150, 190)"]
# fig.update_layout(coloraxis_showscale=False)
#background_color=#2596be
#fig.show()

#getting the company name
#symbol.removesuffix('.ns')
company_name = symbol.removesuffix('.NS')


#Display the close prize
st.header(company_name +' Close prize\n')
st.line_chart(df['Close'])


#st.plotly_chart(fig, use_container_width=True)
st.write(fig)

#Display the Volume
st.header(company_name+' Volume\n')
st.line_chart(df['Volume'])

#Get statistics on the data
st.header('Data Statistics')
st.write(df.describe())

#ticker for financials and more
tk = yf.Ticker(symbol)
st.write(tk.dividends)
st.write(tk.financials)
st.write(tk.splits)
st.write(tk.major_holders)
st.write(tk.cashflow)
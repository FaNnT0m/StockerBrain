import streamlit as st
import pandas as pd
from PIL import Image
import yfinance as yf

import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.write("""


""")

st.sidebar.header('StockerBrain')

stock = pd.read_csv("stockUpdate.csv")
stockName = stock["Company"]
stock.set_index('Company', inplace=True)


def get_input():
    symbol = st.sidebar.selectbox("Stock Name HERE", (stockName))
    s_date = st.sidebar.date_input("Start date")
    e_date = st.sidebar.date_input("End date")
    intervalOfTime = st.sidebar.text_input("Time Interval", "1m")
    return s_date, e_date, symbol, intervalOfTime


# get user input
startDate, endDate, symbol, intervalOfTime = get_input()


symbol = stock.loc[symbol,'Symbol']
newsymbol = symbol +".NS"

timeDiff = endDate - startDate

if timeDiff.days == 0:
    st.header(
        "To get the data for a specific day please enter end date as the date you like to get data and start date as of the previous day.")
    st.subheader(
        "For Example: If you need data for 14 may 2022 then instead of entering start and end date as 14 please enter start date as '13 may 2022' and emd date as '14 may 2022'. ")
else:
    # getting the data
    # df = get_data(symbol, startDate, endDate)
    df = yf.download(tickers=newsymbol, start=startDate, end=endDate, interval=intervalOfTime)

    # Adjusting data
    df["DateTime"] = list(df.index)
    df = df.reset_index(drop=True)

    # Candlestick
    fig = go.Figure(
        data=[go.Candlestick(x=df['DateTime'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    fig.update_layout(yaxis_title=symbol.removesuffix('.NS') + " Price", xaxis_title="Date", template="plotly_dark")
    fig.update_layout(autosize=False, width=1100, height=750, )

    # getting the company name
    company_name = symbol.removesuffix('.NS')

    # showing close price
    noOfRows = df.shape[0]
    if noOfRows <= 2:
        closePrice = df.iloc[-1, 3]
        beforeClosePrice = df.iloc[-1, 3]
    else:
        closePrice = df.iloc[-1, 3]
        beforeClosePrice = df.iloc[-2, 3]
    newClosePrice = "{:.2f}".format(closePrice)
    changeval = "{:.2f}".format(closePrice - beforeClosePrice)
    changePer = "{:.2f}".format(((closePrice - beforeClosePrice) / beforeClosePrice) * 100)

    if closePrice > beforeClosePrice:
        sign = "+"
    else:
        sign = ""

    st.header(f'Last close price: {newClosePrice} {sign} {changeval} ({changePer}%) ')
    # st.subheader(newClosePrice)

    # Display the close prize
    st.header(company_name + ' Close prize\n')
    st.line_chart(df['Close'])

    # Displaying the candlestick chart
    st.write(fig)

    # Display the Volume
    st.header(company_name + ' Volume\n')
    st.line_chart(df['Volume'])

    # Get statistics on the data
    st.header('Data Statistics')
    st.write(df.describe())

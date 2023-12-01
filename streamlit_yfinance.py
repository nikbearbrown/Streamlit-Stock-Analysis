import pandas as pd
import streamlit as st
import yfinance
from datetime import datetime, timedelta

@st.cache_data
def load_data():
    components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S'
                    '%26P_500_companies')[0]
    return components.set_index('Symbol')

@st.cache_data
def load_quotes(asset, start_date, end_date):
    return yfinance.download(asset, start=start_date, end=end_date)

@st.cache_data
def load_sp500(start_date, end_date):
    return yfinance.download('^GSPC', start=start_date, end=end_date)

def calculate_daily_change(data):
    return ((data['Close'] - data['Open']) / data['Open']) * 100

def main():
    components = load_data()
    title = st.empty()
    st.sidebar.title("Options")

    def label(symbol):
        a = components.loc[symbol]
        return symbol + ' - ' + a.Security

    st.sidebar.subheader('Select asset')
    asset = st.sidebar.selectbox('Click below to select a new asset',
                                 components.index.sort_values(), index=3,
                                 format_func=label)
    title.title(components.loc[asset].Security)
    st.table(components.loc[asset])

    start_date = st.sidebar.date_input("Select start date", datetime.now().date() - timedelta(days=10))
    end_date = st.sidebar.date_input("Select end date", datetime.now().date())

    data0 = load_quotes(asset, start_date, end_date)
    data_sp500 = load_sp500(start_date, end_date)

    data = data0.copy().dropna()
    data.index.name = None

    # section = st.sidebar.slider('Number of quotes', min_value=30,
    #                     max_value=min([2000, data.shape[0]]),
    #                     value=500,  step=10)

    data2 = data.copy()

    sma = st.sidebar.checkbox('SMA')
    if sma:
        period = st.sidebar.slider('SMA period', min_value=5, max_value=500,
                             value=20,  step=1)
        data[f'SMA {period}'] = data['Adj Close'].rolling(period).mean()
        data2[f'SMA {period}'] = data[f'SMA {period}'].reindex(data2.index)

    # Calculate daily percentage change
    data2['Daily Change %'] = calculate_daily_change(data2)
    data_sp500['Daily Change %'] = calculate_daily_change(data_sp500)

    st.subheader('Stock Closing Price v/s Moving Average over time')
    if sma:
        st.line_chart(data2[['Adj Close', f'SMA {period}']])
    else:
        st.line_chart(data2['Adj Close'])
    
    st.subheader('Daily Change % Over Time - Comparison')
    chart_data = pd.DataFrame({
        f'{asset} Daily Change %': data2['Daily Change %'],
        'S&P 500 Daily Change %': data_sp500['Daily Change %']
    })
    st.line_chart(chart_data)
    
    st.subheader('Stock Volume over time')
    st.line_chart(data2['Volume'])

    if st.sidebar.checkbox('View statistic'):
        st.subheader('Statistic')
        st.table(data0.describe())

    if st.sidebar.checkbox('View quotes'):
        st.subheader(f'{asset} historical data')
        st.write(data2)

if __name__ == '__main__':
    main()

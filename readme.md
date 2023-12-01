# Streamlit Financial Data Web App

This Streamlit web app allows users to visualize historical stock data, including closing prices, moving averages, daily percentage changes, and volume. Users can compare the selected stock with the S&P 500 index.

## Getting Started

### Prerequisites

Make sure you have Python installed on your machine. You can install the required dependencies using the following:

```
pip install -r requirements.txt
```

### Running the App

To run the app, execute the following command in your terminal:

```
streamlit run streamlit_yfinance.py
```

### Usage
1. Select Asset:

Choose a stock from the S&P 500 list using the dropdown menu.
View additional information about the selected stock.

2. Select Date Range:

Use the date input widgets to choose the start and end dates for the historical data.

3. Options:

Toggle Simple Moving Average (SMA) to display moving averages on the closing price chart.
Adjust the SMA period using the slider.

4. Charts:

View the closing price chart along with SMA if selected.
Compare the daily percentage change of the selected stock with the S&P 500.

5. Statistics and Quotes:

Optionally view statistical information and historical data.

import streamlit as st
import pandas as pd
import requests

@st.cache_data
def fetch_data(api_url):
    response = requests.get(api_url)
    return response.json()

def get_crypto(api_url):
    data = pd.DataFrame(fetch_data(api_url))
    id = data.loc[data['name'] == st.selectbox('Cryptocurrencies', data['name'])]["id"].iloc[0]
    return id

def crypto_market_chart(api_url):
    data = pd.DataFrame(fetch_data(api_url))
    market = pd.DataFrame(data["prices"].tolist(), columns=["date", "price"])
    market['date'] = pd.to_datetime(market['date'], unit='ms')
    market.set_index("date")
    return market

def graph_crypto(market):
    st.title("Historical Market Price ($)")
    st.line_chart(market, x="date",y=["price"])

def compare_crypto(api_url):
    data_list = pd.DataFrame(fetch_data(api_url))
    select = st.multiselect("Compare Two Cryptos", data_list['name'], max_selections=2)
    if (len(select) == 2):
        cr1 = select[0]
        cr2 = select[1]
        cr1 = data_list.loc[data_list["name"] == cr1]["id"].iloc[0]
        cr2 = data_list.loc[data_list["name"] == cr2]["id"].iloc[0]
        cr1 = f"https://api.coingecko.com/api/v3/coins/{cr1}/market_chart?vs_currency=usd&days=365"
        cr1 = crypto_market_chart(cr1)
        cr2 = f"https://api.coingecko.com/api/v3/coins/{cr2}/market_chart?vs_currency=usd&days=365"
        cr2 = crypto_market_chart(cr2)
        crc = cr1
        crc.rename(columns={"price":select[0]}, inplace=True)
        crc[select[1]] = cr2['price']
        st.title("Historical Price Comparison ($)")
        st.line_chart(crc, x="date", y=[select[0],select[1]], y_label="price")

def main():
    api_url = "https://api.coingecko.com/api/v3/coins/list"
    id = get_crypto(api_url)
    api_url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency=usd&days=365"
    market = crypto_market_chart(api_url)
    st.metric('Current Market Price ($)', market['price'].iloc[-1])
    graph_crypto(market)
    api_url = "https://api.coingecko.com/api/v3/coins/list"
    compare_crypto(api_url)

    


if __name__ == "__main__":
    main()

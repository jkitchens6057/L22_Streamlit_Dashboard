from app import *

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

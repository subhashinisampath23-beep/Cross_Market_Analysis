
import streamlit as st
import pandas as pd
import sqlite3


st.title("SQL Query Runner")



db_path = "crypto_market.db"
conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)


# ------------------------------------------------------------
# SQL QUERIES
# ------------------------------------------------------------

queries = {

    "1. Top 3 Cryptocurrencies": """
    SELECT
        id,
        symbol,
        name,
        market_cap,
        market_cap_rank
    FROM cryptocurrencies
    ORDER BY market_cap DESC
    LIMIT 3
    """,

    "2. Supply Exceeds 90%": """
    SELECT
        id,
        name,
        circulating_supply,
        total_supply,
        (circulating_supply / total_supply) * 100
        AS supply_percentage
    FROM cryptocurrencies
    WHERE total_supply IS NOT NULL
      AND total_supply > 0
      AND circulating_supply > 0.90 * total_supply
    """,

    "3. Coins Within 10% of ATH": """
    SELECT
        id,
        name,
        current_price,
        ath,
        (current_price / ath) * 100
        AS percentage_of_ath
    FROM cryptocurrencies
    WHERE ath IS NOT NULL
      AND ath > 0
      AND current_price >= 0.90 * ath
    """,

    "4. Average Market Cap Rank Above $1B Volume": """
    SELECT
        AVG(market_cap_rank)
        AS average_market_cap_rank
    FROM cryptocurrencies
    WHERE total_volume > 1000000000
    """,

    "5. Most Recently Updated Coin": """
    SELECT *
    FROM cryptocurrencies
    ORDER BY date DESC
    LIMIT 1
    """,

    "6. Highest Bitcoin Price": """
    SELECT
        MAX(price_usd) AS highest_bitcoin_price
    FROM crypto_prices
    WHERE coin_id = 'bitcoin'
    """,

    "7. Average Ethereum Price": """
    SELECT
        AVG(price_usd) AS average_ethereum_price
    FROM crypto_prices
    WHERE coin_id = 'ethereum'
    """,

    "8. Highest Oil Price": """
    SELECT
        MAX(price_usd) AS highest_oil_price
    FROM oil_prices
    """,

    "9. Average Oil Price Per Year": """
    SELECT
        strftime('%Y', date) AS year,
        AVG(price_usd) AS average_oil_price
    FROM oil_prices
    GROUP BY strftime('%Y', date)
    ORDER BY year
    """,

    "10. COVID Oil Prices": """
    SELECT
        date,
        price_usd
    FROM oil_prices
    WHERE date BETWEEN '2020-03-01'
    AND '2020-04-30'
    ORDER BY date
    """,

    "11. Lowest Oil Price": """
    SELECT
        date,
        price_usd
    FROM oil_prices
    ORDER BY price_usd ASC
    LIMIT 1
    """,

    "12. Oil Volatility Per Year": """
    SELECT
        strftime('%Y', date) AS year,
        MAX(price_usd) AS maximum_price,
        MIN(price_usd) AS minimum_price,
        MAX(price_usd) - MIN(price_usd)
        AS volatility
    FROM oil_prices
    GROUP BY strftime('%Y', date)
    ORDER BY year
    """,

    "13. Highest NASDAQ Close": """
    SELECT
        MAX(close) AS highest_nasdaq_close
    FROM stock_prices
    WHERE ticker = '^IXIC'
    """,

    "14. Top 5 S&P 500 Price Differences": """
    SELECT
        date,
        high,
        low,
        high - low AS price_difference
    FROM stock_prices
    WHERE ticker = '^GSPC'
    ORDER BY price_difference DESC
    LIMIT 5
    """,

    "15. Monthly Average Closing Price": """
    SELECT
        ticker,
        strftime('%Y-%m', date) AS month,
        AVG(close) AS average_closing_price
    FROM stock_prices
    GROUP BY ticker, strftime('%Y-%m', date)
    ORDER BY month, ticker
    """,

    "16. Average NIFTY Volume 2024": """
    SELECT
        AVG(volume) AS average_nifty_volume
    FROM stock_prices
    WHERE ticker = '^NSEI'
    AND date BETWEEN '2024-01-01'
    AND '2024-12-31'
    """,

    "17. Bitcoin vs Oil": """
    SELECT
        c.date,
        c.price_usd AS bitcoin_price,
        o.price_usd AS oil_price
    FROM crypto_prices c
    INNER JOIN oil_prices o
        ON c.date = o.date
    WHERE c.coin_id = 'bitcoin'
    ORDER BY c.date
    """,

    "18. Bitcoin vs S&P 500": """
    SELECT
        c.date,
        c.price_usd AS bitcoin_price,
        s.close AS sp500_close
    FROM crypto_prices c
    INNER JOIN stock_prices s
        ON c.date = s.date
    WHERE c.coin_id = 'bitcoin'
    AND s.ticker = '^GSPC'
    ORDER BY c.date
    """,

    "19. Ethereum vs NASDAQ": """
    SELECT
        c.date,
        c.price_usd AS ethereum_price,
        s.close AS nasdaq_close
    FROM crypto_prices c
    INNER JOIN stock_prices s
        ON c.date = s.date
    WHERE c.coin_id = 'ethereum'
    AND s.ticker = '^IXIC'
    ORDER BY c.date
    """,

    "20. Bitcoin + Oil + S&P 500": """
    SELECT
        c.date,
        c.price_usd AS bitcoin_price,
        o.price_usd AS oil_price,
        s.close AS sp500_close
    FROM crypto_prices c
    INNER JOIN oil_prices o
        ON c.date = o.date
    INNER JOIN stock_prices s
        ON c.date = s.date
    WHERE c.coin_id = 'bitcoin'
    AND s.ticker = '^GSPC'
    ORDER BY c.date
    """
}


# ------------------------------------------------------------
# SELECT QUERY
# ------------------------------------------------------------

selected_query = st.selectbox(
    "Select a SQL Query",
    list(queries.keys())
)


# ------------------------------------------------------------
# DISPLAY SQL
# ------------------------------------------------------------

st.subheader("SQL Query")

st.code(
    queries[selected_query],
    language="sql"
)


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

if st.button("Run Query"):

    try:

        result = pd.read_sql_query(
            queries[selected_query],
            conn
        )

        st.subheader("Query Result")

        st.dataframe(
            result,
            use_container_width=True
        )

        st.write(
            "Number of records:",
            len(result)
        )

    except Exception as e:

        st.error(
            f"Error executing query: {e}"
        )

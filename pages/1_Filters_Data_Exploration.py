import streamlit as st
import pandas as pd
import sqlite3
import os
import datetime

st.title("Filters & Data Exploration")

db_path = "crypto_market.db"

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)
st.write("Database date check")

check_query = """
SELECT
    MIN(date) AS first_date,
    MAX(date) AS last_date,
    COUNT(*) AS total_records
FROM crypto_prices
"""

check_df = pd.read_sql_query(
    check_query,
    conn
)

st.write(check_df)

selected_dates = st.date_input(
    "Select Date Range",
    value=(
        datetime.date(2025, 1, 1),
        datetime.date(2025, 12, 31)
    )
)

if len(selected_dates) == 2:

    start_date = selected_dates[0]
    end_date = selected_dates[1]

    st.write(
        f"Selected period: {start_date} to {end_date}"
    )

    # --------------------------------------------------------
    # BITCOIN AVERAGE
    # --------------------------------------------------------

    bitcoin_query = """
    SELECT AVG(price_usd) AS average_price
    FROM crypto_prices
    WHERE coin_id = 'bitcoin'
      AND date BETWEEN ? AND ?
    """

    bitcoin_df = pd.read_sql_query(
        bitcoin_query,
        conn,
        params=(start_date, end_date)
    )

    bitcoin_avg = bitcoin_df["average_price"].iloc[0]


    # --------------------------------------------------------
    # OIL AVERAGE
    # --------------------------------------------------------

    oil_query = """
    SELECT AVG(price_usd) AS average_price
    FROM oil_prices
    WHERE date BETWEEN ? AND ?
    """

    oil_df = pd.read_sql_query(
        oil_query,
        conn,
        params=(start_date, end_date)
    )

    oil_avg = oil_df["average_price"].iloc[0]


    # --------------------------------------------------------
    # S&P 500 AVERAGE
    # --------------------------------------------------------

    sp500_query = """
    SELECT AVG(close) AS average_close
    FROM stock_prices
    WHERE ticker = '^GSPC'
      AND date BETWEEN ? AND ?
    """

    sp500_df = pd.read_sql_query(
        sp500_query,
        conn,
        params=(start_date, end_date)
    )

    sp500_avg = sp500_df["average_close"].iloc[0]


    # --------------------------------------------------------
    # NIFTY AVERAGE
    # --------------------------------------------------------

    nifty_query = """
    SELECT AVG(close) AS average_close
    FROM stock_prices
    WHERE ticker = '^NSEI'
      AND date BETWEEN ? AND ?
    """

    nifty_df = pd.read_sql_query(
        nifty_query,
        conn,
        params=(start_date, end_date)
    )

    nifty_avg = nifty_df["average_close"].iloc[0]


    # --------------------------------------------------------
    # DISPLAY SUMMARY
    # --------------------------------------------------------

    st.subheader("Market Summary")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        if pd.notna(bitcoin_avg):

            st.metric(
                "Bitcoin Average",
                f"{bitcoin_avg:,.2f}"
            )

        else:

            st.metric(
                "Bitcoin Average",
                "No data"
            )


    with col2:

        if pd.notna(oil_avg):

            st.metric(
                "Oil Average",
                f"{oil_avg:,.2f}"
            )

        else:

            st.metric(
                "Oil Average",
                "No data"
            )


    with col3:

        if pd.notna(sp500_avg):

            st.metric(
                "S&P 500 Average",
                f"{sp500_avg:,.2f}"
            )

        else:

            st.metric(
                "S&P 500 Average",
                "No data"
            )


    with col4:

        if pd.notna(nifty_avg):

            st.metric(
                "NIFTY Average",
                f"{nifty_avg:,.2f}"
            )

        else:

            st.metric(
                "NIFTY Average",
                "No data"
            )


    # --------------------------------------------------------
    # DAILY MARKET SNAPSHOT
    # --------------------------------------------------------

    st.subheader("Daily Market Snapshot")

    snapshot_query = """
    SELECT
        c.date,
        c.price_usd AS bitcoin_price,
        o.price_usd AS oil_price,
        sp.close AS sp500_close,
        n.close AS nifty_close

    FROM crypto_prices c

    LEFT JOIN oil_prices o
        ON c.date = o.date

    LEFT JOIN stock_prices sp
        ON c.date = sp.date
        AND sp.ticker = '^GSPC'

    LEFT JOIN stock_prices n
        ON c.date = n.date
        AND n.ticker = '^NSEI'

    WHERE c.coin_id = 'bitcoin'
      AND c.date BETWEEN ? AND ?

    ORDER BY c.date
    """

    snapshot_df = pd.read_sql_query(
        snapshot_query,
        conn,
        params=(start_date, end_date)
    )

    st.dataframe(
        snapshot_df,
        use_container_width=True
    )

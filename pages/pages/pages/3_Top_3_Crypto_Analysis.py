import streamlit as st
import pandas as pd
import sqlite3


st.title("Top 3 Crypto Analysis")


# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

db_path = "crypto_market.db"

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)


# ------------------------------------------------------------
# GET TOP 3 CRYPTOCURRENCIES
# ------------------------------------------------------------

top_crypto_query = """
SELECT
    id,
    name,
    symbol,
    market_cap,
    market_cap_rank
FROM cryptocurrencies
ORDER BY market_cap_rank
LIMIT 3
"""

top_crypto_df = pd.read_sql_query(
    top_crypto_query,
    conn
)


# ------------------------------------------------------------
# SELECT CRYPTOCURRENCY
# ------------------------------------------------------------

selected_coin = st.selectbox(
    "Select Cryptocurrency",
    top_crypto_df["id"].tolist()
)


selected_name = top_crypto_df.loc[
    top_crypto_df["id"] == selected_coin,
    "name"
].iloc[0]

st.subheader(selected_name)


# ------------------------------------------------------------
# GET ACTUAL DATE RANGE FOR SELECTED COIN
# ------------------------------------------------------------

date_query = """
SELECT
    MIN(date) AS min_date,
    MAX(date) AS max_date
FROM crypto_prices
WHERE coin_id = ?
"""

date_df = pd.read_sql_query(
    date_query,
    conn,
    params=(selected_coin,)
)

min_date = pd.to_datetime(
    date_df["min_date"].iloc[0]
).date()

max_date = pd.to_datetime(
    date_df["max_date"].iloc[0]
).date()


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

selected_dates = st.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if len(selected_dates) == 2:

    start_date = selected_dates[0]
    end_date = selected_dates[1]


    # --------------------------------------------------------
    # GET DAILY PRICES
    # --------------------------------------------------------

    price_query = """
    SELECT
        date,
        price_usd
    FROM crypto_prices
    WHERE coin_id = ?
      AND date BETWEEN ? AND ?
    ORDER BY date
    """

    price_df = pd.read_sql_query(
        price_query,
        conn,
        params=(
            selected_coin,
            start_date,
            end_date
        )
    )


    # --------------------------------------------------------
    # DAILY PRICE TABLE
    # --------------------------------------------------------

    st.subheader("Daily Price Table")

    st.dataframe(
        price_df,
        use_container_width=True
    )


    # --------------------------------------------------------
    # LINE CHART
    # --------------------------------------------------------

    if not price_df.empty:

        chart_df = price_df.copy()

        chart_df["date"] = pd.to_datetime(
            chart_df["date"]
        )

        chart_df = chart_df.set_index(
            "date"
        )

        st.subheader("Daily Price Trend")

        st.line_chart(
            chart_df["price_usd"]
        )

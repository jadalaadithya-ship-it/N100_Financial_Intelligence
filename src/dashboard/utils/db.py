import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


# Cache the database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)


# -----------------------------
# Companies
# -----------------------------
@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM companies", conn)


# -----------------------------
# Financial Ratios
# -----------------------------
@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    conn = get_connection()

    query = """
        SELECT *
        FROM financial_ratios_computed
        WHERE company_id=?
    """

    params = [ticker]

    if year is not None:
        query += " AND year=?"
        params.append(year)

    return pd.read_sql(query, conn, params=params)


# -----------------------------
# Profit & Loss
# -----------------------------
@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        """,
        conn,
        params=[ticker],
    )


# -----------------------------
# Balance Sheet
# -----------------------------
@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        """,
        conn,
        params=[ticker],
    )


# -----------------------------
# Cash Flow
# -----------------------------
@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        """,
        conn,
        params=[ticker],
    )


# -----------------------------
# Sectors
# -----------------------------
@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    return pd.read_sql(
        "SELECT * FROM sectors",
        conn,
    )


# -----------------------------
# Peer Comparison
# -----------------------------
@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = get_connection()

    return pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name=?
        """,
        conn,
        params=[group_name],
    )


# -----------------------------
# Valuation
# -----------------------------
@st.cache_data(ttl=600)
def get_valuation(ticker):
    conn = get_connection()

    try:
        return pd.read_sql(
            """
            SELECT *
            FROM valuation_summary
            WHERE company_id=?
            """,
            conn,
            params=[ticker],
        )
    except Exception:
        return pd.DataFrame()
@st.cache_data(ttl=600)
def get_companies_with_ratios(year):
    query = """
    SELECT
        c.company_name,
        f.return_on_equity_pct,
        f.net_profit_margin_pct,
        f.debt_to_equity
    FROM companies c
    JOIN financial_ratios_computed f
        ON c.id = f.company_id
    WHERE f.year = ?
    ORDER BY f.return_on_equity_pct DESC
    """

    return pd.read_sql(query, get_connection(), params=(year,))
@st.cache_data(ttl=600)
def get_companies_with_ratios(year):
    query = """
    SELECT
        c.company_name,
        f.return_on_equity_pct,
        f.net_profit_margin_pct,
        f.debt_to_equity
    FROM companies c
    JOIN financial_ratios_computed f
        ON c.id = f.company_id
    WHERE f.year = ?
    ORDER BY f.return_on_equity_pct DESC
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(year,),
    )
@st.cache_data(ttl=600)
def get_company(company_id):
    query = """
    SELECT *
    FROM companies
    WHERE id = ?
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(company_id,),
    )
@st.cache_data(ttl=600)
def get_all_ratios(year):
    query = """
    SELECT
        c.company_name,
        f.return_on_equity_pct,
        f.net_profit_margin_pct,
        f.operating_profit_margin_pct,
        f.debt_to_equity,
        f.asset_turnover
    FROM companies c
    JOIN financial_ratios_computed f
        ON c.id = f.company_id
    WHERE f.year = ?
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(year,),
    )
@st.cache_data(ttl=600)
def get_peer_comparison(year):
    query = """
    SELECT
        pg.peer_group_name,
        c.company_name,
        f.return_on_equity_pct,
        f.net_profit_margin_pct,
        f.debt_to_equity,
        f.asset_turnover
    FROM peer_groups pg
    JOIN companies c
        ON pg.company_id = c.id
    JOIN financial_ratios_computed f
        ON c.id = f.company_id
    WHERE f.year = ?
    ORDER BY pg.peer_group_name, c.company_name
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(year,),
    )
@st.cache_data(ttl=600)
def get_company_trends(company_id):
    query = """
    SELECT
        year,
        return_on_equity_pct,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        debt_to_equity,
        asset_turnover
    FROM financial_ratios_computed
    WHERE company_id = ?
    ORDER BY year
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(company_id,),
    )
@st.cache_data(ttl=600)
def get_sector_summary():
    query = """
    SELECT
        s.broad_sector,
        COUNT(c.id) AS total_companies,
        AVG(c.roe_percentage) AS avg_roe,
        AVG(c.roce_percentage) AS avg_roce
    FROM sectors s
    JOIN companies c
        ON s.company_id = c.id
    GROUP BY s.broad_sector
    ORDER BY total_companies DESC
    """

    return pd.read_sql(query, get_connection())
@st.cache_data(ttl=600)
def get_capital_data(year):
    query = """
    SELECT
        c.company_name,
        m.market_cap_crore,
        m.enterprise_value_crore,
        m.pe_ratio,
        m.pb_ratio,
        m.ev_ebitda,
        m.dividend_yield_pct
    FROM market_cap m
    JOIN companies c
        ON m.company_id = c.id
    WHERE m.year = ?
    ORDER BY m.market_cap_crore DESC
    """

    return pd.read_sql(
        query,
        get_connection(),
        params=(year,),
    )
import pandas as pd
import sqlite3
import streamlit as st

CATEGORY_BUCKETS = {
    "Groceries": "Needs",
    "Transportation": "Needs",
    "Health & Fitness": "Needs",
    "Bills & Utilities": "Needs",
    "Dining Out": "Wants",
    "Entertainment": "Wants",
    "Shopping": "Wants",
    "Savings": "Savings",
    "Other": "Needs"
}

def load_data():
    conn = sqlite3.connect("finances.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            description TEXT,
            category TEXT,
            amount REAL,
            payment_method TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    df = pd.read_sql_query("SELECT * FROM expenses ORDER BY date DESC", conn)
    conn.close()
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], format='mixed').dt.date
    return df

def seed_sample_data():
    conn = sqlite3.connect("finances.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, description TEXT, category TEXT,
        amount REAL, payment_method TEXT, notes TEXT)''')
    conn.commit()
    c.execute("SELECT COUNT(*) FROM expenses")
    count = c.fetchone()[0]

    if count == 0:
        from datetime import date, timedelta

        today = date.today()

        def d(days_ago):
            return str(today - timedelta(days=days_ago))

        sample_expenses = [
            # --- Week 1 (most recent) ---
            (d(1),  "Rent",              "Bills & Utilities", 1500.00, "Credit Card"),
            (d(1),  "Savings deposit",   "Savings",            400.00, "Debit Card"),
            (d(2),  "Groceries",         "Groceries",           95.40, "Debit Card"),
            (d(3),  "Electric bill",     "Bills & Utilities",   85.00, "Debit Card"),
            (d(3),  "Dining Out",        "Dining Out",          42.00, "Credit Card"),
            (d(4),  "Gym membership",    "Health & Fitness",    30.00, "Credit Card"),
            (d(5),  "Uber",              "Transportation",      18.50, "Credit Card"),
            (d(5),  "Coffee shop",       "Dining Out",          12.00, "Cash"),
            (d(6),  "Groceries",         "Groceries",           88.20, "Debit Card"),
            (d(6),  "Netflix",           "Entertainment",       15.99, "Credit Card"),
            (d(7),  "Shopping",          "Shopping",            65.00, "Credit Card"),

            # --- Week 2 ---
            (d(8),  "Savings deposit",   "Savings",            350.00, "Debit Card"),
            (d(9),  "Groceries",         "Groceries",           91.60, "Debit Card"),
            (d(10), "Internet bill",     "Bills & Utilities",   60.00, "Debit Card"),
            (d(11), "Dining Out",        "Dining Out",          55.00, "Credit Card"),
            (d(12), "Transportation",    "Transportation",      40.00, "Debit Card"),
            (d(13), "Shopping",          "Shopping",            80.00, "Credit Card"),
            (d(13), "Groceries",         "Groceries",           74.30, "Debit Card"),
            (d(14), "Entertainment",     "Entertainment",       35.00, "Credit Card"),

            # --- Week 3 ---
            (d(15), "Savings deposit",   "Savings",            400.00, "Debit Card"),
            (d(16), "Groceries",         "Groceries",          102.50, "Debit Card"),
            (d(17), "Phone bill",        "Bills & Utilities",   45.00, "Debit Card"),
            (d(18), "Dining Out",        "Dining Out",          38.00, "Cash"),
            (d(19), "Health & Fitness",  "Health & Fitness",    25.00, "Cash"),
            (d(20), "Uber",              "Transportation",      22.00, "Credit Card"),
            (d(20), "Shopping",          "Shopping",            55.00, "Credit Card"),
            (d(21), "Entertainment",     "Entertainment",       28.00, "Credit Card"),

            # --- Week 4 ---
            (d(22), "Savings deposit",   "Savings",            350.00, "Debit Card"),
            (d(23), "Groceries",         "Groceries",           98.80, "Debit Card"),
            (d(24), "Electric bill",     "Bills & Utilities",   80.00, "Debit Card"),
            (d(25), "Dining Out",        "Dining Out",          48.00, "Credit Card"),
            (d(26), "Transportation",    "Transportation",      35.00, "Debit Card"),
            (d(27), "Shopping",          "Shopping",            70.00, "Credit Card"),
            (d(28), "Entertainment",     "Entertainment",       40.00, "Credit Card"),

            # --- 5-8 weeks ago ---
            (d(32), "Rent",              "Bills & Utilities", 1500.00, "Credit Card"),
            (d(32), "Savings deposit",   "Savings",            400.00, "Debit Card"),
            (d(33), "Groceries",         "Groceries",           89.50, "Debit Card"),
            (d(34), "Dining Out",        "Dining Out",          52.00, "Credit Card"),
            (d(35), "Entertainment",     "Entertainment",       30.00, "Credit Card"),
            (d(36), "Transportation",    "Transportation",      38.00, "Debit Card"),
            (d(37), "Shopping",          "Shopping",            60.00, "Credit Card"),
            (d(38), "Groceries",         "Groceries",           95.00, "Debit Card"),
            (d(40), "Savings deposit",   "Savings",            350.00, "Debit Card"),
            (d(41), "Dining Out",        "Dining Out",          44.00, "Cash"),
            (d(42), "Health & Fitness",  "Health & Fitness",    30.00, "Cash"),
            (d(43), "Bills & Utilities", "Bills & Utilities",   75.00, "Debit Card"),
            (d(44), "Groceries",         "Groceries",           92.00, "Debit Card"),
            (d(45), "Entertainment",     "Entertainment",       25.00, "Credit Card"),
            (d(46), "Shopping",          "Shopping",            85.00, "Credit Card"),
            (d(47), "Transportation",    "Transportation",      30.00, "Debit Card"),
            (d(48), "Savings deposit",   "Savings",            400.00, "Debit Card"),
            (d(50), "Dining Out",        "Dining Out",          60.00, "Credit Card"),
            (d(51), "Groceries",         "Groceries",           88.00, "Debit Card"),
            (d(52), "Rent",              "Bills & Utilities", 1500.00, "Credit Card"),
            (d(53), "Entertainment",     "Entertainment",       35.00, "Credit Card"),
            (d(54), "Shopping",          "Shopping",            75.00, "Credit Card"),
            (d(55), "Transportation",    "Transportation",      42.00, "Debit Card"),
            (d(56), "Savings deposit",   "Savings",            350.00, "Debit Card"),
        ]

        for expense_date, description, category, amount, payment in sample_expenses:
            c.execute('''
                INSERT INTO expenses (date, description, category, amount, payment_method, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (expense_date, description, category, amount, payment, "Sample data"))

        conn.commit()
    conn.close()

def get_week_label(date):
    start = date - pd.Timedelta(days=date.dayofweek)
    end = start + pd.Timedelta(days=6)
    return f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}"

def filter_data(df, time_filter, selected_period):
    if df.empty:
        return df

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format='mixed')

    if time_filter == "Weekly":
        df["period"] = df["date"].apply(get_week_label)
    elif time_filter == "Monthly":
        df["period"] = df["date"].dt.strftime("%B %Y")
    elif time_filter == "Yearly":
        df["period"] = df["date"].dt.strftime("%Y")

    return df[df["period"] == selected_period].drop(columns=["period"])

def get_periods(df, time_filter):
    if df.empty:
        return []

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format='mixed')

    if time_filter == "Weekly":
        df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.dayofweek, unit='d')
        df["period"] = df["date"].apply(get_week_label)
        order = df.drop_duplicates("period").sort_values("week_start", ascending=False)
        return order["period"].tolist()
    elif time_filter == "Monthly":
        df["month_start"] = df["date"].dt.to_period("M").dt.to_timestamp()
        df["period"] = df["date"].dt.strftime("%B %Y")
        order = df.drop_duplicates("period").sort_values("month_start", ascending=False)
        return order["period"].tolist()
    elif time_filter == "Yearly":
        periods = df["date"].dt.strftime("%Y")
        return sorted(periods.unique().tolist(), reverse=True)
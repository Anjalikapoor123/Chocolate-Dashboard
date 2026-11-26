import pandas as pd
import streamlit as st

st.set_page_config(page_title="Chocolate Sales Dashboard", layout="wide")
st.header("Chocolate Sales Dashboard 🍫")

@st.cache_data
def load_data():
    df = pd.read_csv("Chocolate Sales.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    # Amount me $ aur , hata ke number bana diya
    df["Amount"] = pd.to_numeric(df["Amount"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False), errors='coerce')
    df["Boxes Shipped"] = pd.to_numeric(df["Boxes Shipped"], errors='coerce')
    return df

df = load_data()

st.sidebar.header("Dashboard Filters")
prdnam = st.sidebar.multiselect(label="Product", options=df["Product"].dropna().unique())
Salesperson = st.sidebar.multiselect(label="Sales Person", options=df["Sales Person"].dropna().unique())
country = st.sidebar.multiselect(label="Country", options=df["Country"].dropna().unique())
use_date = st.sidebar.checkbox("Filter by Date?")
if use_date:
    date_sel = st.sidebar.date_input("Select Date", value=None)
else:
    date_sel = None

# Shuru me saara data le liya
fil_df = df.copy()

if prdnam:
    fil_df = fil_df[fil_df["Product"].isin(prdnam)]
if Salesperson:
    fil_df = fil_df[fil_df["Sales Person"].isin(Salesperson)]
if country:
    fil_df = fil_df[fil_df["Country"].isin(country)]
if date_sel:
    fil_df = fil_df[fil_df["Date"].dt.date == date_sel]

col1, col2, col3, col4 = st.columns(4)
total_sales = fil_df["Amount"].sum()
Shipped_Boxes = fil_df["Boxes Shipped"].sum()

# Agar Boxes 0 hai to divide nahi hoga, isliye check lagaya
if Shipped_Boxes == 0:
    revenue_per_box = 0
else:
    revenue_per_box = total_sales / Shipped_Boxes

avg_sale = fil_df["Amount"].mean()

col1.metric("Total Amount", total_sales)
col2.metric("Total sales", Shipped_Boxes)
col3.metric("Total Revenue Generated", revenue_per_box)
col4.metric("Average Sale", avg_sale)
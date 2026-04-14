import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- CONFIG ----------
st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide"
)

BASE_DIR = Path("dashboard_data")
DATASETS = ["DATA1", "DATA2", "DATA3"]

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
dataset = st.sidebar.selectbox("Select dataset", DATASETS)

data_path = BASE_DIR / dataset

# ---------- LOAD FUNCTION ----------
@st.cache_data
def load_dataset(path: Path):
    data = {}

    # CSVs
    data["authors"] = pd.read_csv(path / "author_popularity.csv")
    data["daily_revenue"] = pd.read_csv(path / "daily_revenue.csv")
    data["top_days"] = pd.read_csv(path / "top_5_days.csv")
    data["top_customer"] = pd.read_csv(path / "top_customer_details.csv")

    # TXT metrics
    with open(path / "unique_users.txt") as f:
        data["unique_users"] = int(f.read().strip())

    with open(path / "unique_authors.txt") as f:
        data["unique_authors"] = int(f.read().strip())

    with open(path / "top_customer_total_spent.txt") as f:
        data["top_customer_spent"] = float(f.read().strip())

    return data


data = load_dataset(data_path)

# ---------- HEADER ----------
st.title(f"📊 EDA Dashboard — {dataset}")

# ---------- KPI SECTION ----------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Unique Users", data["unique_users"])
col2.metric("Unique Authors", data["unique_authors"])
col3.metric("Top Customer Spend", f"${data['top_customer_spent']:,.2f}")

# ---------- TOP CUSTOMER ----------
st.subheader("🏆 Top Customer Details")
st.dataframe(data["top_customer"], use_container_width=True)

# ---------- TOP 5 DAYS ----------
st.subheader("📅 Top 5 Days by Revenue")
st.dataframe(data["top_days"], use_container_width=True)

# ---------- AUTHOR POPULARITY ----------
st.subheader("📚 Most Popular Authors")

authors_df = data["authors"].copy()

# Optional: sort for safety
authors_df = authors_df.sort_values(by=authors_df.columns[1], ascending=False)

st.bar_chart(
    authors_df.set_index(authors_df.columns[0])
)

# ---------- DAILY REVENUE ----------
st.subheader("📈 Daily Revenue Trend")

rev_df = data["daily_revenue"].copy()
rev_df[rev_df.columns[0]] = pd.to_datetime(rev_df[rev_df.columns[0]])

rev_df = rev_df.sort_values(by=rev_df.columns[0])

st.line_chart(
    rev_df.set_index(rev_df.columns[0])
)

# ---------- DOWNLOAD SECTION ----------
st.subheader("⬇️ Download Data")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Download Daily Revenue",
        data["daily_revenue"].to_csv(index=False),
        file_name=f"{dataset}_daily_revenue.csv"
    )

with col2:
    st.download_button(
        "Download Author Popularity",
        data["authors"].to_csv(index=False),
        file_name=f"{dataset}_author_popularity.csv"
    )

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Precomputed EDA results • Fast loading • No recomputation")
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

# ---------- LOAD FUNCTION ----------
@st.cache_data
def load_dataset(path: Path):
    data = {}

    data["authors"] = pd.read_csv(path / "author_popularity.csv")
    data["daily_revenue"] = pd.read_csv(path / "daily_revenue.csv")
    data["top_days"] = pd.read_csv(path / "top_5_days.csv")
    data["top_customer"] = pd.read_csv(path / "top_customer_details.csv")

    with open(path / "unique_users.txt") as f:
        data["unique_users"] = int(f.read().strip())

    with open(path / "unique_authors.txt") as f:
        data["unique_authors"] = int(f.read().strip())

    with open(path / "top_customer_total_spent.txt") as f:
        data["top_customer_spent"] = float(f.read().strip())

    return data


# ---------- UI ----------
st.title("📊 EDA Dashboard")

tabs = st.tabs(DATASETS)

# ---------- TAB CONTENT ----------
for tab, dataset in zip(tabs, DATASETS):

    with tab:
        data_path = BASE_DIR / dataset
        data = load_dataset(data_path)

        st.header(dataset)

        # ---------- KPI ----------
        col1, col2, col3 = st.columns(3)

        col1.metric("Unique Users", data["unique_users"])
        col2.metric("Unique Authors", data["unique_authors"])
        col3.metric("Top Customer Spend", f"${data['top_customer_spent']:,.2f}")

        # ---------- AUTHORS PROCESSING ----------
        authors_df = data["authors"].copy()

        # Dynamically detect columns
        author_col = authors_df.columns[0]
        value_col = authors_df.columns[1]

        # Sort descending
        authors_df = authors_df.sort_values(by=value_col, ascending=False)

        # ---------- TOP AUTHOR ----------
        st.subheader("⭐ Top Author")

        top_author = authors_df.iloc[0]

        col1, col2 = st.columns([1, 2])

        col1.metric("Author", top_author[author_col])
        col2.metric("Purchases / Count", int(top_author[value_col]))

        # ---------- TOP 5 AUTHORS ----------
        st.subheader("🏆 Top 5 Authors")

        top5 = authors_df.head(5)

        chart_df = top5.set_index(author_col)

        st.bar_chart(chart_df[value_col])

        st.dataframe(top5, use_container_width=True)

        # ---------- TOP CUSTOMER ----------
        st.subheader("👤 Top Customer")
        st.dataframe(data["top_customer"], use_container_width=True)

        # ---------- TOP DAYS ----------
        st.subheader("📅 Top 5 Revenue Days")
        st.dataframe(data["top_days"], use_container_width=True)

        # ---------- DAILY REVENUE ----------
        st.subheader("📈 Daily Revenue")

        rev_df = data["daily_revenue"].copy()

        date_col = rev_df.columns[0]
        revenue_col = rev_df.columns[1]

        rev_df[date_col] = pd.to_datetime(rev_df[date_col])
        rev_df = rev_df.sort_values(by=date_col)

        st.line_chart(
            rev_df.set_index(date_col)[revenue_col]
        )

        # ---------- DOWNLOAD ----------
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

        st.markdown("---")

# ---------- FOOTER ----------
st.caption("Precomputed EDA results • Fast • No recomputation")
import streamlit as st
import pandas as pd
from database import fetch_records

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Patient Logs", layout="wide")

st.title("📋 Patient Records Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
rows, columns = fetch_records()

if not rows:
    st.warning("No records found")
    st.stop()

df = pd.DataFrame(rows, columns=columns)

# -------------------------------
# CLEAN DATA
# -------------------------------
if "symptoms" in df.columns:
    df["symptoms"] = df["symptoms"].apply(
        lambda x: str(x)[:60] + "..." if len(str(x)) > 60 else x
    )

# -------------------------------
# FILTER SECTION
# -------------------------------
st.subheader("🔍 Filters")

col1, col2, col3 = st.columns(3)

with col1:
    name_search = st.text_input("Search by Name")

with col2:
    disease_filter = st.selectbox(
        "Disease",
        ["All"] + sorted(df["disease"].dropna().unique().tolist())
    )

with col3:
    min_conf = st.slider("Min Confidence", 0, 100, 0)

# -------------------------------
# APPLY FILTERS
# -------------------------------
filtered_df = df.copy()

if name_search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(name_search, case=False, na=False)
    ]

if disease_filter != "All":
    filtered_df = filtered_df[
        filtered_df["disease"] == disease_filter
    ]

filtered_df = filtered_df[
    filtered_df["confidence"] >= min_conf
]

# -------------------------------
# DISPLAY
# -------------------------------
st.success(f"Showing {len(filtered_df)} / {len(df)} records")

st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# DOWNLOAD OPTION
# -------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    "patient_records.csv",
    "text/csv"
)

# -------------------------------
# REFRESH
# -------------------------------
if st.button("🔄 Refresh"):
    st.rerun()
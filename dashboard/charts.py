import streamlit as st
import pandas as pd

def render_summary(df: pd.DataFrame):
    st.subheader("Summary")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Alerts", len(df))
    col2.metric("Disaster Types", df["disaster_type"].nunique() if "disaster_type" in df else 0)
    col3.metric("High Severity", int((df["severity"] == "HIGH").sum()) if "severity" in df else 0)
    col4.metric("Sources", df["source"].nunique() if "source" in df else 0)

def render_charts(df: pd.DataFrame):
    st.subheader("Dashboard")

    if df.empty:
        st.info("필터 조건에 맞는 데이터가 없습니다.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Disaster Type Distribution")
        if "disaster_type" in df:
            st.bar_chart(df["disaster_type"].value_counts())

    with col2:
        st.markdown("#### Severity Distribution")
        if "severity" in df:
            st.bar_chart(df["severity"].value_counts())

    st.markdown("#### Source Distribution")
    if "source" in df:
        st.bar_chart(df["source"].value_counts())

import streamlit as st
import pandas as pd

from collectors.rss_collector import collect_from_rss_sources
from analyzer.disaster_classifier import classify_alerts
from translator.translator import translate_alerts
from database.db import init_db, save_alerts, load_alerts
from dashboard.charts import render_summary, render_charts
from notifier.discord import send_discord_alert
from reports.report_generator import generate_disaster_report

st.set_page_config(page_title="Japan Disaster Alert Monitor", page_icon="🚨", layout="wide")

st.title("🚨 Japan Disaster Alert Monitor")
st.caption("일본 재난 속보 수집 → 재난 유형 분류 → 한국어 번역 → 대시보드 시각화 → 알림/리포트 생성")

init_db()

with st.sidebar:
    st.header("Data Source")
    mode = st.radio("수집 방식", ["Sample Data", "RSS URL"])

    if mode == "RSS URL":
        rss_url = st.text_input("RSS URL", value="https://www3.nhk.or.jp/rss/news/cat0.xml")
        max_items = st.slider("가져올 기사 수", 5, 50, 20)
    else:
        rss_url = ""
        max_items = 20

    st.markdown("---")
    use_translation = st.checkbox("한국어 번역 실행", value=True)

    st.markdown("---")
    st.header("Notification")
    discord_webhook_url = st.text_input("Discord Webhook URL", type="password")
    notify_high_only = st.checkbox("HIGH 위험도만 알림", value=True)

st.subheader("1. Alert Collection")

if st.button("재난 속보 수집 및 분석", type="primary"):
    if mode == "RSS URL":
        alerts = collect_from_rss_sources([rss_url], max_items=max_items)
    else:
        alerts = collect_from_rss_sources([], use_sample=True)

    classified = classify_alerts(alerts)
    translated = translate_alerts(classified) if use_translation else classified

    save_alerts(translated)
    st.session_state["alerts"] = translated

if "alerts" not in st.session_state:
    st.session_state["alerts"] = load_alerts()

alerts = st.session_state["alerts"]

if not alerts:
    st.info("왼쪽 설정을 확인한 뒤 '재난 속보 수집 및 분석' 버튼을 눌러주세요.")
    st.stop()

df = pd.DataFrame(alerts)

render_summary(df)

st.subheader("2. Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    disaster_options = ["전체"] + sorted(df["disaster_type"].dropna().unique().tolist())
    selected_disaster = st.selectbox("재난 유형", disaster_options)

with filter_col2:
    severity_options = ["전체"] + sorted(df["severity"].dropna().unique().tolist())
    selected_severity = st.selectbox("위험도", severity_options)

with filter_col3:
    keyword = st.text_input("키워드 검색", placeholder="예: 地震, 津波, 台風, 미야기")

filtered_df = df.copy()

if selected_disaster != "전체":
    filtered_df = filtered_df[filtered_df["disaster_type"] == selected_disaster]

if selected_severity != "전체":
    filtered_df = filtered_df[filtered_df["severity"] == selected_severity]

if keyword:
    keyword_lower = keyword.lower()
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: keyword_lower in str(row.to_dict()).lower(),
            axis=1
        )
    ]

st.subheader("3. Disaster Alerts")
st.dataframe(filtered_df, use_container_width=True)

render_charts(filtered_df)

st.subheader("4. Alert Details")

for _, row in filtered_df.iterrows():
    severity_icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟢"}.get(row.get("severity", "LOW"), "🟢")

    with st.expander(f"{severity_icon} {row.get('disaster_type', '기타')} | {row.get('title_ja', '')}"):
        st.markdown(f"**Source**: {row.get('source', '')}")
        st.markdown(f"**Published**: {row.get('published', '')}")
        st.markdown(f"**Disaster Type**: {row.get('disaster_type', '')}")
        st.markdown(f"**Severity**: {row.get('severity', '')}")

        st.markdown("#### Japanese Original")
        st.write(row.get("summary_ja", ""))

        st.markdown("#### Korean Translation")
        st.write(row.get("summary_ko", ""))

        alert_message = f"""
🚨 일본 재난 속보 알림

유형: {row.get('disaster_type', '')}
위험도: {row.get('severity', '')}
제목: {row.get('title_ko', row.get('title_ja', ''))}
요약: {row.get('summary_ko', '')}
링크: {row.get('link', '')}
"""
        st.markdown("#### Alert Message")
        st.code(alert_message.strip(), language="text")

        if discord_webhook_url:
            should_send = row.get("severity") == "HIGH" if notify_high_only else True
            if should_send and st.button(f"Discord 알림 전송 - {row.get('title_ja', '')[:20]}", key=row.get("id", row.get("title_ja", ""))):
                ok, msg = send_discord_alert(discord_webhook_url, alert_message)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        if row.get("link"):
            st.markdown(f"[Original Link]({row.get('link')})")

st.subheader("5. Disaster Report")

report = generate_disaster_report(filtered_df)
st.text_area("Markdown Report", report, height=280)

col_a, col_b = st.columns(2)

with col_a:
    csv_data = filtered_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", data=csv_data, file_name="japan_disaster_alerts.csv", mime="text/csv")

with col_b:
    st.download_button("Markdown 리포트 다운로드", data=report, file_name="disaster_report.md", mime="text/markdown")

from datetime import datetime
import pandas as pd

def generate_disaster_report(df: pd.DataFrame) -> str:
    lines = [
        "# Japan Disaster Alert Report",
        "",
        f"- Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Total Alerts: {len(df)}",
        "",
        "## Summary",
        "",
    ]

    if df.empty:
        lines.append("분석 대상 재난 속보가 없습니다.")
        return "\n".join(lines)

    type_counts = df["disaster_type"].value_counts().to_dict()
    severity_counts = df["severity"].value_counts().to_dict()

    lines.append("### Disaster Type Distribution")
    for key, value in type_counts.items():
        lines.append(f"- {key}: {value}")

    lines.append("")
    lines.append("### Severity Distribution")
    for key, value in severity_counts.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Alert Details", ""])

    for _, row in df.iterrows():
        lines.extend([
            f"### {row.get('title_ko') or row.get('title_ja')}",
            "",
            f"- Original Title: {row.get('title_ja', '')}",
            f"- Type: {row.get('disaster_type', '')}",
            f"- Severity: {row.get('severity', '')}",
            f"- Published: {row.get('published', '')}",
            f"- Matched Keywords: {row.get('matched_keywords', '')}",
            f"- Link: {row.get('link', '')}",
            "",
            "#### Korean Summary",
            "",
            str(row.get("summary_ko", "")),
            "",
        ])

    return "\n".join(lines)

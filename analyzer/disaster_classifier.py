from typing import List, Dict

DISASTER_KEYWORDS = {
    "지진": ["地震", "震度", "震源", "マグニチュード", "M"],
    "쓰나미": ["津波", "津波注意報", "津波警報"],
    "태풍": ["台風", "暴風", "強風"],
    "폭우": ["大雨", "豪雨", "線状降水帯", "洪水", "土砂災害"],
    "화산": ["火山", "噴火", "噴煙", "火口"],
    "폭설": ["大雪", "積雪", "吹雪"],
    "폭염": ["猛暑", "熱中症", "高温"],
}

HIGH_KEYWORDS = ["警報", "避難", "命を守る", "津波警報", "噴火", "特別警報"]
MEDIUM_KEYWORDS = ["注意報", "強い", "大雨", "震度", "台風"]

def classify_alerts(alerts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    results = []

    for alert in alerts:
        text = f"{alert.get('title_ja', '')} {alert.get('summary_ja', '')}"

        disaster_type = "기타"
        matched_keywords = []

        for dtype, keywords in DISASTER_KEYWORDS.items():
            found = [keyword for keyword in keywords if keyword in text]
            if found:
                disaster_type = dtype
                matched_keywords = found
                break

        enriched = dict(alert)
        enriched["disaster_type"] = disaster_type
        enriched["severity"] = _estimate_severity(text)
        enriched["matched_keywords"] = ", ".join(matched_keywords)
        results.append(enriched)

    return results

def _estimate_severity(text: str) -> str:
    if any(keyword in text for keyword in HIGH_KEYWORDS):
        return "HIGH"
    if any(keyword in text for keyword in MEDIUM_KEYWORDS):
        return "MEDIUM"
    return "LOW"

import json
from pathlib import Path
from typing import List, Dict
import feedparser

SAMPLE_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "sample_alerts.json"

def collect_from_rss_sources(rss_urls: List[str], max_items: int = 20, use_sample: bool = False) -> List[Dict[str, str]]:
    if use_sample or not rss_urls:
        return _load_sample_alerts()

    alerts = []

    for url in rss_urls:
        feed = feedparser.parse(url)

        for entry in feed.entries[:max_items]:
            alerts.append({
                "source": feed.feed.get("title", "RSS Source"),
                "title_ja": entry.get("title", ""),
                "summary_ja": entry.get("summary", entry.get("description", "")),
                "published": entry.get("published", ""),
                "link": entry.get("link", ""),
            })

    return alerts

def _load_sample_alerts() -> List[Dict[str, str]]:
    with SAMPLE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

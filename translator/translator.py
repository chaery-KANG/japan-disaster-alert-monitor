from typing import List, Dict

try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None

def translate_alerts(alerts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    results = []

    translator = None
    if GoogleTranslator is not None:
        try:
            translator = GoogleTranslator(source="ja", target="ko")
        except Exception:
            translator = None

    for alert in alerts:
        enriched = dict(alert)
        title_ja = alert.get("title_ja", "")
        summary_ja = alert.get("summary_ja", "")

        if translator is None:
            enriched["title_ko"] = "[번역 비활성화] " + title_ja
            enriched["summary_ko"] = "[번역 비활성화] " + summary_ja
        else:
            try:
                enriched["title_ko"] = translator.translate(title_ja) if title_ja else ""
                enriched["summary_ko"] = translator.translate(summary_ja[:4500]) if summary_ja else ""
            except Exception:
                enriched["title_ko"] = "[번역 실패] " + title_ja
                enriched["summary_ko"] = "[번역 실패] " + summary_ja

        results.append(enriched)

    return results

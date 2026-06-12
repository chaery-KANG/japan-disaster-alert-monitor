# Architecture

Japan Disaster Alert Monitor는 일본 재난 정보를 수집하고 한국어로 번역하여 시각화하는 모니터링 시스템입니다.

## Pipeline

```text
RSS / Sample Data
    ↓
Collector
    ↓
Disaster Classifier
    ↓
Japanese-Korean Translator
    ↓
SQLite Storage
    ↓
Streamlit Dashboard
    ↓
Discord Notification
    ↓
Markdown Report / CSV Export
```

## Modules

| Module | Description |
|---|---|
| collectors | RSS 또는 샘플 데이터 수집 |
| analyzer | 재난 키워드 기반 유형 분류 |
| translator | 일본어 원문을 한국어로 번역 |
| database | SQLite 저장 및 조회 |
| dashboard | Streamlit 시각화 |
| notifier | Discord Webhook 알림 |
| reports | Markdown 리포트 생성 |

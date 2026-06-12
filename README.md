# Japan Disaster Alert Monitor

일본 재난 정보를 자동 수집하여 한국어로 번역하고 시각화하는 재난 속보 모니터링 시스템입니다.

## 개발 배경

일본 체류 중 NHK 및 일본 언론의 재난 속보를 모니터링하면서, 일본어로 제공되는 긴급 정보를 한국어로 신속하게 파악하기 어렵다는 점을 느꼈습니다.

이에 따라 일본 재난 정보를 자동 수집하고, 재난 유형을 분류한 뒤, 한국어로 번역하여 확인할 수 있는 `Japan Disaster Alert Monitor`를 개발하였습니다.

## v2 Update

- 재난 유형 필터
- 위험도 필터
- 키워드 검색
- Discord Webhook 알림
- Markdown 리포트 생성
- CSV 다운로드
- 알림 메시지 자동 생성
- 매칭 키워드 표시

## Features

- 일본 재난 RSS 수집
- 샘플 재난 데이터 분석
- 재난 유형 자동 분류
- 위험도 분류
- 일본어 → 한국어 자동 번역
- SQLite 저장
- Streamlit 대시보드
- Discord 알림
- Markdown 리포트 생성
- CSV 다운로드

## Disaster Types

| Type | Keywords |
|---|---|
| 지진 | 地震, 震度, 震源, マグニチュード |
| 쓰나미 | 津波, 津波注意報, 津波警報 |
| 태풍 | 台風, 暴風, 強風 |
| 폭우 | 大雨, 豪雨, 線状降水帯, 洪水 |
| 화산 | 火山, 噴火, 噴煙 |
| 폭설 | 大雪, 積雪 |
| 폭염 | 猛暑, 熱中症 |

## Tech Stack

- Python
- Streamlit
- Feedparser
- Deep Translator
- SQLite
- Pandas
- Discord Webhook

## Architecture

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

## Project Structure

```text
japan-disaster-alert-monitor
├─ app.py
├─ collectors
│  └─ rss_collector.py
├─ analyzer
│  └─ disaster_classifier.py
├─ translator
│  └─ translator.py
├─ database
│  └─ db.py
├─ dashboard
│  └─ charts.py
├─ notifier
│  └─ discord.py
├─ reports
│  └─ report_generator.py
├─ sample_data
│  └─ sample_alerts.json
├─ docs
│  └─ architecture.md
├─ requirements.txt
└─ README.md
```

## How to Run

### 1. 가상환경 생성

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 라이브러리 설치

```powershell
pip install -r requirements.txt
```

### 3. 실행

```powershell
streamlit run app.py
```

## Usage

### Sample Data 모드

샘플 데이터 기반으로 바로 재난 유형 분류와 한국어 번역을 테스트할 수 있습니다.

### RSS URL 모드

RSS URL을 입력하면 해당 RSS에서 최신 항목을 가져와 분석합니다.

기본 예시 URL:

```text
https://www3.nhk.or.jp/rss/news/cat0.xml
```

### Discord 알림

Discord Webhook URL을 입력하면 HIGH 위험도 재난 속보를 Discord로 전송할 수 있습니다.

## Demo Screenshot

이미지를 추가할 경우 아래 형식으로 README에 삽입할 수 있습니다.

```markdown
![Dashboard](./images/dashboard.png)
![Alert Detail](./images/alert-detail.png)
![Report](./images/report.png)
```

## Portfolio Point

이 프로젝트는 단순 뉴스 수집기가 아니라, 재난 정보 수집·분류·번역·저장·시각화·알림·리포트 생성을 하나의 파이프라인으로 구현한 모니터링 시스템입니다.

일본 현지 뉴스 모니터링 경험과 연결하여 실제 필요성 기반 프로젝트로 설명할 수 있습니다.

## GitHub Commit Example

```powershell
git init
git add .
git commit -m "feat: initialize Japan disaster alert monitor"
git branch -M main
git remote add origin https://github.com/chaery-KANG/japan-disaster-alert-monitor.git
git push -u origin main
```

## Future Improvements

- Telegram 알림
- Google Sheets 저장
- 지도 기반 지역 시각화
- JMA 공식 데이터 연동
- 재난별 심각도 세부 점수화
- 자동 주기 실행 스케줄러

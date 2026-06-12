from typing import Tuple
import requests

def send_discord_alert(webhook_url: str, message: str) -> Tuple[bool, str]:
    if not webhook_url:
        return False, "Discord Webhook URL이 없습니다."

    try:
        response = requests.post(webhook_url, json={"content": message}, timeout=10)
        if response.status_code in (200, 204):
            return True, "Discord 알림을 전송했습니다."
        return False, f"Discord 전송 실패: HTTP {response.status_code} / {response.text}"
    except Exception as e:
        return False, f"Discord 전송 중 오류가 발생했습니다: {e}"

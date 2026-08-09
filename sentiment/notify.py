from __future__ import annotations

import json
import os
from datetime import datetime, timezone

import requests

from sentiment.models import SentimentReading


def _format_message(readings: list[SentimentReading]) -> str:
    lines = []
    for reading in readings:
        line = f"{reading.emoji} {reading.asset}: {reading.score:.0f}/100 — {reading.label}"
        if reading.detail:
            line += f"\n   {reading.detail}"
        lines.append(line)
    return "\n\n".join(lines)


def send_push_notification(readings: list[SentimentReading]) -> None:
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        raise RuntimeError("NTFY_TOPIC environment variable is required")

    server = os.environ.get("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    token = os.environ.get("NTFY_TOKEN")

    today = datetime.now(timezone.utc).strftime("%b %d, %Y")
    title = f"Market Sentiment — {today}"
    message = _format_message(readings)
    tags = ["chart_with_upwards_trend", "money_with_wings", "gem"]

    headers = {
        "Title": title,
        "Tags": ",".join(tags),
        "Priority": "default",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{server}/{topic}",
        data=json.dumps(
            {
                "topic": topic,
                "message": message,
                "title": title,
                "tags": tags,
                "priority": 3,
            }
        ).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json; charset=utf-8"},
        timeout=30,
    )
    response.raise_for_status()

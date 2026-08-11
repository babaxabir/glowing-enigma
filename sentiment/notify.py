from __future__ import annotations

import os
from datetime import datetime, timezone

import requests

from sentiment.models import SentimentReading

DEFAULT_NTFY_SERVER = "https://ntfy.sh"


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default).strip()
    return value or default


def _format_message(readings: list[SentimentReading]) -> str:
    lines = []
    for reading in readings:
        line = f"{reading.emoji} {reading.asset}: {reading.score:.0f}/100 — {reading.label}"
        if reading.detail:
            line += f"\n   {reading.detail}"
        lines.append(line)
    return "\n\n".join(lines)


def send_push_notification(readings: list[SentimentReading]) -> None:
    topic = _env("NTFY_TOPIC")
    if not topic:
        raise RuntimeError("NTFY_TOPIC environment variable is required")

    server = _env("NTFY_SERVER", DEFAULT_NTFY_SERVER).rstrip("/")
    if not server.startswith(("http://", "https://")):
        raise RuntimeError(
            "NTFY_SERVER must include a scheme, e.g. https://ntfy.sh "
            f"(got: {server!r})"
        )

    token = _env("NTFY_TOKEN")

    today = datetime.now(timezone.utc).strftime("%b %d, %Y")
    title = f"Market Sentiment — {today}"
    message = _format_message(readings)
    tags = ["chart_with_upwards_trend", "money_with_wings", "gem"]

    headers = {
        "Title": title,
        "Tags": ",".join(tags),
        "Priority": "3",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{server}/{topic}",
        data=message.encode("utf-8"),
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

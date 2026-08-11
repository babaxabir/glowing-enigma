from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

from sentiment.models import SentimentReading

DEFAULT_NTFY_SERVER = "https://ntfy.sh"
VALID_TOPIC_PATTERN = re.compile(r"^[-_A-Za-z0-9]{1,64}$")
ASSET_COLUMN_WIDTH = 10
METRIC_SEPARATOR = " · "


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default).strip()
    return value or default


def _normalize_topic(raw_topic: str) -> str:
    topic = raw_topic.strip()

    if topic.startswith(("http://", "https://")):
        path = urlparse(topic).path.strip("/")
        topic = path.split("/")[-1] if path else topic
    elif "ntfy.sh/" in topic:
        topic = topic.rsplit("ntfy.sh/", 1)[-1].strip("/")

    topic = topic.strip().strip("/")
    return topic


def _validate_topic(topic: str) -> None:
    if not topic:
        raise RuntimeError(
            "NTFY_TOPIC is empty. Set a GitHub secret with your ntfy topic name."
        )
    if not VALID_TOPIC_PATTERN.fullmatch(topic):
        raise RuntimeError(
            "NTFY_TOPIC is invalid for ntfy. Use 1-64 characters: letters, "
            "numbers, underscores, and dashes only. "
            f"Got: {topic!r}. Example: market-sentiment-a8f3k2"
        )


def _format_message(readings: list[SentimentReading]) -> str:
    lines = ["DAILY MARKET SENTIMENT", ""]

    for reading in readings:
        name = reading.asset.ljust(ASSET_COLUMN_WIDTH)
        lines.append(f"{name} {reading.score:>3.0f}/100  {reading.label}")
        if reading.metrics:
            metric_line = METRIC_SEPARATOR.join(reading.metrics)
            lines.append(f"{' ' * ASSET_COLUMN_WIDTH} {metric_line}")
        lines.append("")

    return "\n".join(lines).rstrip()


def validate_notification_config() -> str:
    """Validate config before fetching data so missing secrets fail fast."""
    topic = _normalize_topic(_env("NTFY_TOPIC"))
    _validate_topic(topic)
    return topic


def send_push_notification(readings: list[SentimentReading]) -> None:
    topic = validate_notification_config()

    server = _env("NTFY_SERVER", DEFAULT_NTFY_SERVER).rstrip("/")
    if not server.startswith(("http://", "https://")):
        raise RuntimeError(
            "NTFY_SERVER must include a scheme, e.g. https://ntfy.sh "
            f"(got: {server!r})"
        )

    token = _env("NTFY_TOKEN")

    today = datetime.now(timezone.utc).strftime("%b %d, %Y")
    title = f"Market Sentiment | {today}"
    message = _format_message(readings)
    tags = "bar_chart,oil_drum,bitcoin"

    headers = {
        "Title": title,
        "Tags": tags,
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
    if response.status_code == 400:
        raise RuntimeError(
            f"ntfy rejected the request (400). Check NTFY_TOPIC={topic!r} "
            "uses only letters, numbers, underscores, and dashes."
        ) from None
    response.raise_for_status()

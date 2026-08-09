from __future__ import annotations

import requests

from sentiment.models import SentimentReading

CNN_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
BTC_URL = "https://api.alternative.me/fng/?limit=1"
CNN_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.cnn.com",
    "Referer": "https://edition.cnn.com/markets/fear-and-greed",
}


def _title_case_label(label: str) -> str:
    return " ".join(word.capitalize() for word in label.replace("_", " ").split())


def fetch_btc_sentiment() -> SentimentReading:
    response = requests.get(BTC_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if payload.get("metadata", {}).get("error"):
        raise RuntimeError(payload["metadata"]["error"])

    latest = payload["data"][0]
    score = float(latest["value"])
    label = _title_case_label(latest["value_classification"])

    return SentimentReading(
        asset="Bitcoin",
        score=score,
        label=label,
        source="Alternative.me Crypto Fear & Greed Index",
        detail="Higher scores indicate greed; lower scores indicate fear.",
    )


def fetch_sp500_sentiment() -> SentimentReading:
    response = requests.get(CNN_URL, headers=CNN_HEADERS, timeout=30)
    response.raise_for_status()
    payload = response.json()

    current = payload.get("fear_and_greed")
    if not current:
        raise RuntimeError("CNN response missing fear_and_greed data")

    score = float(current["score"])
    label = _title_case_label(current["rating"])
    week_ago = current.get("previous_1_week")
    detail = f"Week ago: {week_ago:.0f}" if week_ago is not None else ""

    return SentimentReading(
        asset="S&P 500",
        score=score,
        label=label,
        source="CNN Fear & Greed Index",
        detail=detail,
    )

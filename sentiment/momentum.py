from __future__ import annotations

import yfinance as yf

from sentiment.models import SentimentReading


def score_to_label(score: float) -> str:
    if score >= 75:
        return "Extreme Greed"
    if score >= 55:
        return "Greed"
    if score >= 45:
        return "Neutral"
    if score >= 25:
        return "Fear"
    return "Extreme Fear"


def _rsi(closes: list[float], period: int = 14) -> float:
    if len(closes) <= period:
        return 50.0

    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(closes[-period - 1 : -1], closes[-period:]):
        delta = current - previous
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period
    if average_loss == 0:
        return 100.0

    rs = average_gain / average_loss
    return 100.0 - (100.0 / (1.0 + rs))


def _pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100.0


def price_change_metrics(ticker: str) -> tuple[str, str]:
    history = yf.Ticker(ticker).history(period="90d", auto_adjust=True)
    if history.empty or len(history) < 6:
        raise RuntimeError(f"Unable to fetch enough price history for {ticker}")

    closes = history["Close"].tolist()
    latest = closes[-1]
    week_ago = closes[-6] if len(closes) >= 6 else closes[0]
    month_ago = closes[-22] if len(closes) >= 22 else closes[0]

    week_change = _pct_change(latest, week_ago)
    month_change = _pct_change(latest, month_ago)
    return f"7d {week_change:+.1f}%", f"30d {month_change:+.1f}%"


def fetch_momentum_sentiment(ticker: str, asset: str, source: str) -> SentimentReading:
    history = yf.Ticker(ticker).history(period="90d", auto_adjust=True)
    if history.empty or len(history) < 30:
        raise RuntimeError(f"Unable to fetch enough price history for {ticker}")

    closes = history["Close"].tolist()
    latest = closes[-1]
    week_ago = closes[-6] if len(closes) >= 6 else closes[0]
    month_ago = closes[-22] if len(closes) >= 22 else closes[0]

    week_change = _pct_change(latest, week_ago)
    month_change = _pct_change(latest, month_ago)
    rsi = _rsi(closes)

    momentum_score = 50.0 + (week_change * 2.5) + (month_change * 1.0)
    score = max(0.0, min(100.0, (momentum_score * 0.55) + (rsi * 0.45)))
    label = score_to_label(score)

    return SentimentReading(
        asset=asset,
        score=score,
        label=label,
        source=source,
        metrics=(
            f"7d {week_change:+.1f}%",
            f"30d {month_change:+.1f}%",
            f"RSI {rsi:.0f}",
        ),
    )


def fetch_gold_sentiment() -> SentimentReading:
    return fetch_momentum_sentiment(
        ticker="GC=F",
        asset="Gold",
        source="Gold futures (GC=F) momentum + RSI",
    )


def fetch_oil_sentiment() -> SentimentReading:
    return fetch_momentum_sentiment(
        ticker="CL=F",
        asset="Oil",
        source="WTI crude (CL=F) momentum + RSI",
    )

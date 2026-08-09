from __future__ import annotations

import sys

from sentiment.fetchers import fetch_btc_sentiment, fetch_sp500_sentiment
from sentiment.gold import fetch_gold_sentiment
from sentiment.notify import send_push_notification


def main() -> int:
    readings = [
        fetch_gold_sentiment(),
        fetch_btc_sentiment(),
        fetch_sp500_sentiment(),
    ]

    for reading in readings:
        print(f"{reading.asset}: {reading.score:.0f}/100 ({reading.label})")

    send_push_notification(readings)
    print("Push notification sent.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - CLI entrypoint should report failures clearly
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

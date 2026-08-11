from __future__ import annotations

import sys

from sentiment.fetchers import fetch_btc_sentiment, fetch_sp500_sentiment
from sentiment.momentum import fetch_gold_sentiment, fetch_oil_sentiment
from sentiment.notify import send_push_notification, validate_notification_config


def main() -> int:
    validate_notification_config()

    readings = [
        fetch_gold_sentiment(),
        fetch_oil_sentiment(),
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

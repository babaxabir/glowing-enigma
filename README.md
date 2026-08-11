# Daily Market Sentiment Push Notifications

Get a daily push notification with sentiment readings for **Gold**, **Bitcoin**, and the **S&P 500**.

This repo runs on a GitHub Actions schedule and sends notifications through [ntfy.sh](https://ntfy.sh) — a free, open-source push service with iOS and Android apps.

## What you receive

Each morning you'll get a notification like:

```
😊 Gold: 62/100 — Greed
   7d +1.2% | 30d +4.8% | RSI 58

😰 Bitcoin: 31/100 — Fear

😊 S&P 500: 64/100 — Greed
   Week ago: 45
```

### Data sources

| Asset | Source |
|-------|--------|
| **Bitcoin** | [Alternative.me Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/) |
| **S&P 500** | [CNN Fear & Greed Index](https://edition.cnn.com/markets/fear-and-greed) |
| **Gold** | Gold futures (GC=F) momentum + RSI via Yahoo Finance |

Gold does not have a standard public fear/greed index, so this project derives a 0–100 score from recent price momentum and RSI, using the same label bands as the other indices.

## Setup (5 minutes)

### 1. Install the ntfy app

Download **ntfy** on your phone:

- [iOS App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
- [Google Play](https://play.google.com/store/apps/details?id=io.hedgewig.ntfy)

### 2. Subscribe to a private topic

1. Open the ntfy app → **+** → **Subscribe to topic**
2. Pick a unique, hard-to-guess topic name (e.g. `market-sentiment-a8f3k2-yourname`)
3. Tap **Subscribe**

> **Important:** Anyone who knows your topic name can send you messages. Use a long random string and never share it publicly.

> **Topic format:** Use only letters, numbers, dashes, and underscores (no spaces or full URLs). Good: `market-sentiment-a8f3k2`. Bad: `market sentiment`, `https://ntfy.sh/my-topic`.

### 3. Add GitHub secrets

In your GitHub repo go to **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Required | Description |
|--------|----------|-------------|
| `NTFY_TOPIC` | Yes | The topic name only (e.g. `market-sentiment-a8f3k2`), not a full URL |
| `NTFY_TOKEN` | No | Bearer token if your topic is access-protected |
| `NTFY_SERVER` | No | Custom ntfy server URL (default: `https://ntfy.sh`) |

### 4. Enable the workflow

The workflow in `.github/workflows/daily-sentiment.yml` runs **every day at 8:00 AM UTC**.

To test immediately:

1. Go to **Actions → Daily Market Sentiment**
2. Click **Run workflow → Run workflow**

You should receive a push notification within a minute.

## Troubleshooting

### `NTFY_TOPIC is empty` or "Missing NTFY_TOPIC secret"

The GitHub secret is not set. Fix it:

1. Open **github.com/babaxabir/glowing-enigma** → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `NTFY_TOPIC` (exact spelling)
4. Value: your topic name only, e.g. `market-sentiment-a8f3k2`
5. Re-run **Actions → Daily Market Sentiment → Run workflow**

Use **Secrets**, not **Variables**. The value must match exactly what you subscribed to in the ntfy app.

### `400 Bad Request` from ntfy

Topic name has invalid characters. Use only letters, numbers, dashes, and underscores — no spaces, no full URLs.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export NTFY_TOPIC="your-topic-name"
python -m sentiment.main
```

Copy `.env.example` to `.env` and load it with your shell if you prefer.

## Customize the schedule

Edit the cron expression in `.github/workflows/daily-sentiment.yml`:

```yaml
schedule:
  - cron: "0 8 * * *"   # 8:00 AM UTC daily
```

Use [crontab.guru](https://crontab.guru/) to pick a different time. GitHub Actions schedules use UTC.

## Project structure

```
sentiment/
  main.py       # Entry point
  fetchers.py   # BTC and S&P 500 sentiment APIs
  gold.py       # Gold momentum/RSI sentiment
  notify.py     # ntfy push delivery
  models.py     # Shared data types
.github/workflows/daily-sentiment.yml
```

## License

MIT

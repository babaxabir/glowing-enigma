# Daily Market Sentiment Push Notifications

Get a daily push notification with sentiment readings for **Gold**, **Oil**, **Bitcoin**, and the **S&P 500**.

This repo runs on a GitHub Actions schedule and sends notifications through [ntfy.sh](https://ntfy.sh) — a free, open-source push service with iOS and Android apps.

## What you receive

Each morning you'll get a notification like:

```
DAILY MARKET SENTIMENT

Gold        78/100  Extreme Greed
           7d +8.7% · 30d +11.4% · RSI 71

Oil         63/100  Greed
           7d +9.0% · 30d +5.7% · RSI 45

Bitcoin     29/100  Fear
           7d +0.0% · 30d -3.3%

S&P 500     65/100  Greed
           1w ago 60 · 1m ago 47
```

### Data sources

| Asset | Source |
|-------|--------|
| **Gold** | Gold futures (GC=F) momentum + RSI via Yahoo Finance |
| **Oil** | WTI crude futures (CL=F) momentum + RSI via Yahoo Finance |
| **Bitcoin** | [Alternative.me Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/) + BTC price trend |
| **S&P 500** | [CNN Fear & Greed Index](https://edition.cnn.com/markets/fear-and-greed) |

Gold and oil do not have standard public fear/greed indices, so this project derives a 0–100 score from recent price momentum and RSI, using the same label bands as the other indices.

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
  momentum.py   # Gold and oil momentum/RSI sentiment
  notify.py     # ntfy push delivery
  models.py     # Shared data types
.github/workflows/daily-sentiment.yml
```

## License

MIT

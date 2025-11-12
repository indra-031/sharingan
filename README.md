# SHARINGAN — The Eye That Sees Beyond ⚡

SHARINGAN is a lightweight RSS aggregator designed for **bug bounty hunters** to discover high-quality writeups, research, and vulnerability reports from multiple sources. It automatically sends notifications to **Telegram** and **Discord** for newly discovered writeups.

---

## Features

- Aggregates feeds from multiple security sources (Medium, PortSwigger, Bugcrowd, Talos, etc.)
- Randomly selects entries from RSS feeds
- Limits sends per run to avoid spam (configurable)
- Persists sent links to prevent duplicates
- Logs metadata (timestamp, title, link, source) for reference
- Fully automated via **cron jobs**

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/sharingan.git
cd sharingan
```
2. Install dependencies:
```
pip3 install -r requirements.txt
```
3. Add your feeds to rss_feeds.txt (one URL per line).
4. Configure Discord & Telegram webhooks/bots in sharingan.py.

## Usage

Run manually:
```
python3 sharingan.py
```
Or schedule with cron (every 6 hours):
```
0 */6 * * * /usr/bin/python3 /opt/sharingan/sharingan.py >> /opt/sharingan/sharingan.log 2>&1
```
## Configuration
-RSS_FEEDS_FILE — File containing RSS feed URLs
-SENT_LINKS_FILE — Keeps track of already sent links
-SIGHTINGS_FILE — Logs metadata for sent entries
-MAX_SENDS_PER_RUN — Maximum number of entries sent per run
-DISCORD_WEBHOOK — Discord webhook URL
-TELEGRAM_BOT_TOKEN — Telegram bot token
-TELEGRAM_CHAT_ID — Telegram chat ID
-TELEGRAM_THREAD_ID — Telegram thread ID (optional)

## Example Feeds
https://portswigger.net/research/rss
https://infosecwriteups.com/feed
https://medium.com/feed/tag/bug-bounty
https://www.hackerone.com/blog/rss.xml

Developed by Indra ⚡

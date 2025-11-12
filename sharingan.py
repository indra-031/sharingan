#!/usr/bin/env python3
# ============================================================
# 👁️ SHARINGAN — The Eye That Sees Beyond
# ⚡ Developed by Indra 
# ============================================================

import feedparser
import requests
import os
import re
from datetime import datetime, timezone
from random import shuffle

# ===================== Configuration =====================
RSS_FEEDS_FILE = "rss_feeds.txt"
SENT_LINKS_FILE = "sent_links.txt"
SIGHTINGS_FILE = "sharingan_sightings.txt"

DISCORD_WEBHOOK = "DISCORD_WEBHOOK_HERE"
TELEGRAM_BOT_TOKEN = "TELEGRAM_TOKEN_HERE"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID_HERE"
TELEGRAM_THREAD_ID = None # TELEGRAM_TOPIC_HERE

MAX_SENDS_PER_RUN = 30
MAX_TELEGRAM_CHARS = 4000
# ============================================================

# -------------------- Utilities --------------------
def ensure_file_exists(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("")

def load_sent_links():
    ensure_file_exists(SENT_LINKS_FILE)
    with open(SENT_LINKS_FILE, "r", encoding="utf-8") as fh:
        return set(line.strip() for line in fh if line.strip())

def append_sent_links(links):
    if links:
        with open(SENT_LINKS_FILE, "a", encoding="utf-8") as fh:
            for link in links:
                fh.write(link + "\n")

def append_sightings_meta(entries):
    if entries:
        with open(SIGHTINGS_FILE, "a", encoding="utf-8") as fh:
            for ts, title, link, source in entries:
                fh.write(f"{ts} | {title} | {link} | {source}\n")

def escape_markdown(text):
    return re.sub(r'([_*[\]()~`>#+-=|{}.!])', r'\\\1', text)

# -------------------- RSS helpers --------------------
def load_rss_feeds():
    if not os.path.exists(RSS_FEEDS_FILE):
        print(f"⚠️ RSS feeds file not found: {RSS_FEEDS_FILE}")
        return []
    with open(RSS_FEEDS_FILE, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

def safe_get_entry_link(entry):
    link = getattr(entry, "link", None)
    if link:
        return link
    links = getattr(entry, "links", []) or []
    if isinstance(links, (list, tuple)) and links:
        first = links[0]
        if isinstance(first, dict):
            return first.get("href")
    return None

def get_source_from_feed(feed_url):
    try:
        from urllib.parse import urlparse
        host = urlparse(feed_url).netloc or feed_url
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return feed_url

# -------------------- Notification senders --------------------
def send_discord_notification(title, link):
    if not DISCORD_WEBHOOK:
        return
    payload = {
        "content": f"👁️ **SHARINGAN has seen something new!**\n📖 {title}\n🔗 {link}",
        "username": "⚡ SHARINGAN"
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=10).raise_for_status()
    except requests.RequestException as e:
        print(f"[Discord] failed: {e}")

def send_telegram_notification(title, link):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    msg = f"👁️ *SHARINGAN detected new knowledge!*\n\n📖 *{escape_markdown(title)}*\n🔗 {link}"
    if len(msg) > MAX_TELEGRAM_CHARS:
        msg = msg[:MAX_TELEGRAM_CHARS-3] + "..."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "message_thread_id": TELEGRAM_THREAD_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10).raise_for_status()
    except requests.RequestException as e:
        print(f"[Telegram] failed: {e}")

# -------------------- Core --------------------
def activate_sharingan():
    ensure_file_exists(SENT_LINKS_FILE)
    ensure_file_exists(SIGHTINGS_FILE)

    feeds = load_rss_feeds()
    sent_links = load_sent_links()
    to_record_sent = []
    sightings_meta = []
    sent_count = 0

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("👁️  SHARINGAN — Activating vision")
    print(f"📅  {datetime.now(timezone.utc).isoformat(sep=' ', timespec='seconds')}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📚 Loaded {len(feeds)} feeds.")
    print(f"⚙️  Max sends per run: {MAX_SENDS_PER_RUN}\n")

    shuffle(feeds)  # randomize feed order
    for feed_url in feeds:
        if sent_count >= MAX_SENDS_PER_RUN:
            break
        print(f"🔎 Scanning: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
            src = get_source_from_feed(feed_url)
            entries = getattr(feed, "entries", []) or []
            shuffle(entries)  # randomize entries
            for entry in entries:
                if sent_count >= MAX_SENDS_PER_RUN:
                    break
                link = safe_get_entry_link(entry)
                if not link or link in sent_links:
                    continue
                title = getattr(entry, "title", "") or getattr(entry, "summary", "") or "Untitled"
                print(f"⚡ New finding: {title} — {link}")
                try:
                    send_discord_notification(title, link)
                    send_telegram_notification(title, link)
                except Exception as e:
                    print(f"❌ Notification error: {e}")
                sent_links.add(link)
                to_record_sent.append(link)
                ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
                sightings_meta.append((ts, title, link, src))
                sent_count += 1
        except Exception as e:
            print(f"❌ Error parsing feed {feed_url}: {e}")

    if to_record_sent:
        append_sent_links(to_record_sent)
        append_sightings_meta(sightings_meta)
        print(f"\n💾 Recorded {len(to_record_sent)} sent link(s) to {SENT_LINKS_FILE}")
        print(f"📝 Added {len(sightings_meta)} metadata line(s) to {SIGHTINGS_FILE}")
    else:
        print("\n😴 No new items were sent this run.")

    print("🏁 SHARINGAN — Deactivating vision.\n")

# -------------------- Entry --------------------
if __name__ == "__main__":
    activate_sharingan()


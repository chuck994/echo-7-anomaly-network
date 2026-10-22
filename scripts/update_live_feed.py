#!/usr/bin/env python3
"""Refresh ECHO-7's public-source signal feed from NASA's public RSS feed.

This is a lightweight public-news feed, not a UAP sighting tracker and not an
AI system. It stores the original article title, URL, publication date, and
short description so the site can display source-linked updates.
"""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "live-updates.json"
FEEDS = [
    {
        "name": "NASA News",
        "url": "https://www.nasa.gov/feed/",
        "topics": ["uap", "unidentified anomalous", "exoplanet", "extraterrestrial",
                   "astrobiology", "life beyond earth", "planet", "asteroid",
                   "meteor", "space telescope", "solar system", "moon", "mars"],
    }
]
MAX_ITEMS = 30


def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", value).strip()


def parse_date(value):
    if not value:
        return ""
    try:
        dt = parsedate_to_datetime(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return ""


def main():
    collected = []
    errors = []
    for feed in FEEDS:
        request = urllib.request.Request(
            feed["url"],
            headers={"User-Agent": "ECHO-7-Public-Signal-Feed/1.0 (+GitHub Actions)"},
        )
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                xml_data = response.read(4_000_000)
            root = ET.fromstring(xml_data)
            for item in root.findall(".//item"):
                title = plain_text(item.findtext("title"))
                url = (item.findtext("link") or "").strip()
                description = plain_text(item.findtext("description"))
                published_raw = item.findtext("pubDate") or ""
                haystack = (title + " " + description).lower()
                matched = [topic for topic in feed["topics"] if topic in haystack]
                # Keep a modest general NASA news sample as well as topic matches.
                if not title or not url:
                    continue
                collected.append({
                    "title": title,
                    "url": url,
                    "source": feed["name"],
                    "publishedAt": parse_date(published_raw),
                    "summary": description[:420],
                    "matchedTopics": matched[:5],
                })
        except Exception as exc:  # retain a useful status instead of failing silently
            errors.append({"source": feed["name"], "message": str(exc)[:240]})

    collected.sort(key=lambda item: item.get("publishedAt", ""), reverse=True)
    payload = {
        "title": "ECHO-7 Public Signal Feed",
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "status": "ok" if collected else "unavailable",
        "notice": "Automatically collected public NASA news headlines. This is not a verified UAP sighting feed and does not imply extraterrestrial origin.",
        "feeds": [{"name": f["name"], "url": f["url"]} for f in FEEDS],
        "errors": errors,
        "items": collected[:MAX_ITEMS],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {min(len(collected), MAX_ITEMS)} items to {OUTPUT}; errors={len(errors)}")


if __name__ == "__main__":
    main()

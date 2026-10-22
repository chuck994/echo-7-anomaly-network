#!/usr/bin/env python3
"""Refresh ECHO-7's public-source snapshots.

Community posts are unverified leads. This script does not authenticate posters
or establish that a reported event was extraterrestrial.
"""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NOW = lambda: datetime.now(timezone.utc).isoformat()
FEEDS = [
    {"name": "NASA News", "url": "https://www.nasa.gov/feed/", "kind": "official"},
    {"name": "r/UFOs (community)", "url": "https://www.reddit.com/r/UFOs/.rss", "kind": "reddit"},
    {"name": "r/UFOB (community reports)", "url": "https://www.reddit.com/r/UFOB/.rss", "kind": "reddit"},
    {"name": "r/Experiencers (personal accounts)", "url": "https://www.reddit.com/r/Experiencers/.rss", "kind": "reddit"},
    {"name": "r/UFOs search: South Carolina", "url": "https://www.reddit.com/r/UFOs/search.rss?q=South%20Carolina&restrict_sr=1&sort=new", "kind": "local"},
    {"name": "r/Charleston search: UFO", "url": "https://www.reddit.com/r/Charleston/search.rss?q=UFO%20OR%20UAP%20OR%20strange%20lights&restrict_sr=1&sort=new", "kind": "local"},
    {"name": "r/southcarolina search: UFO", "url": "https://www.reddit.com/r/southcarolina/search.rss?q=UFO%20OR%20UAP%20OR%20strange%20lights&restrict_sr=1&sort=new", "kind": "local"},
]
LOCAL_TERMS = ["south carolina", "charleston", "mount pleasant", "mount pleasant, sc",
               "lowcountry", "myrtle beach", "columbia, sc", "greenville, sc",
               "hilton head", "beaufort, sc", "summerville", "goose creek", "folly beach"]
FIRSTHAND_TERMS = ["i saw", "i witnessed", "i observed", "my video", "my footage",
                   "i recorded", "i was there", "i experienced", "my experience",
                   "i work", "i worked", "when i served", "i served", "my unit",
                   "i was stationed", "i was a", "i personally", "firsthand", "first hand"]
MAX_ITEMS = 30

def plain_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", value, flags=re.S)
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
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError, OverflowError):
            return ""

def local_match(item):
    haystack = (item["title"] + " " + item["summary"] + " " + item["source"]).lower()
    return any(term in haystack for term in LOCAL_TERMS)

def fetch_feed(feed):
    request = urllib.request.Request(feed["url"], headers={
        "User-Agent": "Mozilla/5.0 (compatible; ECHO-7-OpenResearch/1.0; public RSS reader)"
    })
    with urllib.request.urlopen(request, timeout=22) as response:
        xml_data = response.read(4_000_000)
    root = ET.fromstring(xml_data)
    nodes = root.findall(".//item")
    if not nodes:
        nodes = [node for node in root.iter() if node.tag.lower().endswith("entry")]
    items = []
    for node in nodes:
        title = plain_text(next((e.text for e in node if e.tag.lower().endswith("title")), ""))
        summary = plain_text(next((e.text for e in node if e.tag.lower().endswith(("description", "summary", "content"))), ""))
        url = ""
        for child in node:
            if child.tag.lower().endswith("link"):
                url = child.attrib.get("href", "") or (child.text or "").strip()
                if url:
                    break
        published = next((e.text for e in node if e.tag.lower().endswith(("pubdate", "published", "updated", "date"))), "")
        if not title or not url:
            continue
        text = (title + " " + summary).lower()
        items.append({
            "title": title, "url": url, "source": feed["name"],
            "publishedAt": parse_date(published), "summary": summary[:480],
            "sourceType": feed["kind"],
            "firsthand": feed["kind"] in ("reddit", "local") and any(term in text for term in FIRSTHAND_TERMS),
        })
    return items

def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    all_items, errors = [], []
    for feed in FEEDS:
        try:
            all_items.extend(fetch_feed(feed))
        except Exception as exc:
            errors.append({"source": feed["name"], "message": str(exc)[:220]})
    seen = set()
    unique = []
    for item in sorted(all_items, key=lambda x: x.get("publishedAt", ""), reverse=True):
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        unique.append(item)
    sc_items = [item for item in unique if item["sourceType"] == "local" or local_match(item)]
    community_items = [item for item in unique if item["sourceType"] in ("reddit", "local")]
    DATA.mkdir(parents=True, exist_ok=True)
    common_notice = ("Automatically collected public RSS snapshots. Reddit/community posts are unverified leads, "
                     "not confirmed sightings; firsthand-style labels are keyword hints, not identity verification.")
    write_json(DATA / "live-updates.json", {
        "title": "ECHO-7 Public Signal Feed", "updatedAt": NOW(),
        "status": "ok" if unique else "unavailable", "notice": common_notice,
        "feeds": [{"name": f["name"], "url": f["url"]} for f in FEEDS],
        "errors": errors, "items": unique[:MAX_ITEMS],
    })
    write_json(DATA / "south-carolina-feed.json", {
        "title": "ECHO-7 South Carolina Community Watch", "updatedAt": NOW(),
        "status": "ok" if sc_items else "unavailable",
        "notice": "Community RSS search snapshot for South Carolina and nearby areas. Posts may be jokes, speculation, reposts, or mistaken observations. Verify each original account, time, place, and media independently.",
        "feeds": [{"name": f["name"], "url": f["url"]} for f in FEEDS if f["kind"] == "local"],
        "errors": errors, "items": sc_items[:MAX_ITEMS],
    })
    print(f"Public feed: {min(len(unique), MAX_ITEMS)} items; South Carolina feed: {min(len(sc_items), MAX_ITEMS)}; source errors: {len(errors)}")

if __name__ == "__main__":
    main()

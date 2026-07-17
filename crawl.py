#!/usr/bin/env python3
"""AdScout crawler.

Two layers:
  (a) discovery via RSS / arXiv API  -> must be reliable
  (b) full-text fetch                -> best effort; on failure we store the
      feed/API summary and mark `full_text: pending` in frontmatter.

The pipeline never hard-fails: every exception is caught, degraded, and the
process always exits 0. All *analysis* rules live in SKILL.md — this script
only does fetch / filter / dedupe / frontmatter / file IO.

Usage:
  python crawl.py                                        # crawl all sources.yaml sources
  python crawl.py --url URL --tier N --lang xx --track t # ingest one article (live-demo path)
"""

import argparse
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"

ARXIV_API = "https://export.arxiv.org/api/query"

# Fetch strategies, tried in order. Max 2 — anti-bot fights are out of scope.
UA_BROWSER = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
UA_BOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
FETCH_STRATEGIES = [UA_BROWSER, UA_BOT]
TIMEOUT = 20

COMPANY_BY_DOMAIN = {
    "engineering.fb.com": "meta",
    "netflixtechblog.com": "netflix",
    "arxiv.org": "bytedance",  # seed corpus: ByteDance LongRetriever; override with --company
    "gm7.org": "kuaishou",
    "www.gm7.org": "kuaishou",
    "contexthints.com": "openai-ecosystem",
    "www.contexthints.com": "openai-ecosystem",
    "cloro.dev": "openai-ecosystem",
    "mediapost.com": "openai-ecosystem",
    "www.mediapost.com": "openai-ecosystem",
    "nbcnews.com": "cloudflare",
    "www.nbcnews.com": "cloudflare",
    "mobiledevmemo.com": "analyst",
}


def log(msg):
    print(f"[adscout] {msg}")


def slugify(text, max_len=70):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return text[:max_len].rstrip("-") or "untitled"


def norm_url(url):
    # strip fragments AND query strings (Medium RSS appends ?source=rss----…
    # tracking params that would defeat dedupe against clean URLs)
    return (url or "").split("#")[0].split("?")[0].rstrip("/")


def existing_urls():
    """source_url -> filename for every file already in corpus/ (dedupe key)."""
    seen = {}
    for path in sorted(CORPUS.glob("*.md")):
        try:
            fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            if fm.get("source_url"):
                seen[norm_url(fm["source_url"])] = path.name
        except Exception as exc:  # a malformed file must not kill the crawl
            log(f"warn: could not parse {path.name}: {exc}")
    return seen


def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return yaml.safe_load(match.group(1)) if match else {}


def guess_company(url):
    host = urlparse(url).netloc.lower()
    if "pinterest" in url.lower():
        return "pinterest"
    for domain, company in COMPANY_BY_DOMAIN.items():
        if host == domain or host.endswith("." + domain):
            return company
    return "analyst"


def fetch_html(url):
    """Best-effort fetch. Two strategies max, then give up (returns None)."""
    for ua in FETCH_STRATEGIES:
        try:
            resp = requests.get(url, headers={"User-Agent": ua}, timeout=TIMEOUT)
            if resp.status_code == 200 and resp.text:
                return resp.text
            log(f"  fetch HTTP {resp.status_code} with UA '{ua[:30]}...'")
        except Exception as exc:
            log(f"  fetch error: {type(exc).__name__}: {exc}")
    return None


def extract_text(html):
    """Pull the main article text out of a page. Returns (title, text)."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()
    container = soup.find("article") or soup.find("main") or soup.body or soup
    paragraphs = []
    for el in container.find_all(["h1", "h2", "h3", "p", "li", "blockquote"]):
        text = el.get_text(" ", strip=True)
        if len(text) > 2:
            prefix = {"h1": "# ", "h2": "## ", "h3": "### ", "li": "- "}.get(el.name, "")
            paragraphs.append(prefix + text)
    body = "\n\n".join(paragraphs)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return title, body


def write_article(meta, body):
    """Write one corpus file with frontmatter. Returns the path."""
    fields = ["title", "source_url", "company", "date", "evidence_tier",
              "language", "track", "full_text"]
    ordered = {k: meta.get(k, "") for k in fields}
    fm = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True,
                        default_flow_style=False).strip()
    path = CORPUS / f"{slugify(meta['title'])}.md"
    path.write_text(f"---\n{fm}\n---\n\n{body.strip()}\n", encoding="utf-8")
    return path


def ingest_url(url, tier, lang, track, company=None, summary="", title="",
               feed_body="", pub_date="", seen=None):
    """Ingest a single article. Full text is best effort; always writes a file
    unless the URL is already in the corpus."""
    seen = seen if seen is not None else existing_urls()
    if norm_url(url) in seen:
        log(f"skip (already in corpus): {url}")
        return None

    body, fetched_title, status = "", "", "pending"
    if feed_body and len(feed_body) > 500:  # full_text_in_feed sources
        fetched_title, body = extract_text(feed_body)
        status = "complete"
    else:
        html = fetch_html(url)
        if html:
            fetched_title, body = extract_text(html)
            if len(body) > 500:
                status = "complete"
            else:  # got a page but no real article (paywall/anti-bot shell)
                body = ""

    if status == "pending":
        body = summary.strip() or "(full text pending — fetch failed, see source_url)"
        body = "> Full text unavailable at crawl time; summary below.\n\n" + body

    meta = {
        "title": title or fetched_title or url,
        "source_url": norm_url(url),
        "company": company or guess_company(url),
        "date": pub_date or date.today().isoformat(),
        "evidence_tier": int(tier),
        "language": lang,
        "track": track,
        "full_text": status,
    }
    path = write_article(meta, body)
    seen[norm_url(url)] = path.name
    log(f"wrote {path.name} (full_text: {status})")
    return path


def entry_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        parsed = entry.get(key)
        if parsed:
            return datetime(*parsed[:3]).date().isoformat()
    return ""


def entry_matches(entry, keywords):
    if not keywords:
        return True
    haystack = (entry.get("title", "") + " " + entry.get("summary", "")).lower()
    # word-boundary match: "ads" must not match "uploads"/"heads"
    return any(re.search(r"\b" + re.escape(kw.lower()) + r"\b", haystack)
               for kw in keywords)


def feed_full_body(entry):
    content = entry.get("content") or []
    return content[0].get("value", "") if content else ""


def crawl_source(source, seen):
    name = source.get("name", "?")
    log(f"source: {name}")
    if source.get("type") == "arxiv_api":
        params = {
            "search_query": source["query"],
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": 10,
        }
        resp = requests.get(ARXIV_API, params=params, timeout=TIMEOUT)
        feed = feedparser.parse(resp.text)
    else:
        feed = feedparser.parse(source["url"])

    if not feed.entries:
        log(f"  no entries (feed unreachable or empty) — moving on")
        return

    for entry in feed.entries:
        try:
            if not entry_matches(entry, source.get("filter_keywords")):
                continue
            summary = BeautifulSoup(entry.get("summary", ""),
                                    "html.parser").get_text(" ", strip=True)
            ingest_url(
                url=entry.get("link", ""),
                tier=source.get("default_tier", 4),
                lang=source.get("language", "en"),
                track=source.get("track", "modeling"),
                summary=summary,
                title=entry.get("title", ""),
                feed_body=feed_full_body(entry) if source.get("full_text_in_feed") else "",
                pub_date=entry_date(entry),
                seen=seen,
            )
        except Exception as exc:
            log(f"  item error ({type(exc).__name__}: {exc}) — moving on")


def crawl_all():
    with open(ROOT / "sources.yaml", encoding="utf-8") as fh:
        config = yaml.safe_load(fh)
    seen = existing_urls()
    for source in config.get("sources", []):
        try:
            crawl_source(source, seen)
        except Exception as exc:
            log(f"source error ({type(exc).__name__}: {exc}) — moving on")
    log("crawl complete")


def main():
    parser = argparse.ArgumentParser(description="AdScout crawler")
    parser.add_argument("--url", help="ingest a single article URL")
    parser.add_argument("--tier", type=int, default=4, help="evidence tier 1-4")
    parser.add_argument("--lang", default="en", help="en | zh")
    parser.add_argument("--track", default="modeling",
                        help="modeling | ai_era_ads | infra")
    parser.add_argument("--company", default=None,
                        help="override company (default: inferred from domain)")
    parser.add_argument("--title", default=None, help="override title")
    args = parser.parse_args()

    CORPUS.mkdir(exist_ok=True)
    if args.url:
        ingest_url(args.url, args.tier, args.lang, args.track,
                   company=args.company, title=args.title or "")
    else:
        crawl_all()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # constraint: the pipeline never hard-fails
        log(f"fatal-but-contained: {type(exc).__name__}: {exc}")
    sys.exit(0)

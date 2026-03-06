"""Tavily web search for last30days skill.

Uses the Tavily Search API as the primary web search backend,
replacing Brave Search which was returning 422 errors.

API docs: https://docs.tavily.com/
"""

import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from . import http

ENDPOINT = "https://api.tavily.com/search"

# Domains to exclude (handled by Reddit/X search)
EXCLUDED_DOMAINS = [
    "reddit.com", "www.reddit.com", "old.reddit.com",
    "twitter.com", "www.twitter.com", "x.com", "www.x.com",
]

DEPTH_CONFIG = {"quick": 8, "default": 15, "deep": 20}


def search_web(
    topic: str,
    from_date: str,
    to_date: str,
    api_key: str,
    depth: str = "default",
) -> List[Dict[str, Any]]:
    """Search the web via Tavily Search API.

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        api_key: Tavily API key
        depth: 'quick', 'default', or 'deep'

    Returns:
        List of result dicts with keys: url, title, snippet, source_domain, date, relevance

    Raises:
        http.HTTPError: On API errors
    """
    count = DEPTH_CONFIG.get(depth, 15)
    search_depth = "advanced" if depth == "deep" else "basic"

    # Calculate lookback days
    try:
        d1 = datetime.strptime(from_date, "%Y-%m-%d")
        d2 = datetime.strptime(to_date, "%Y-%m-%d")
        days = max(1, (d2 - d1).days)
    except (ValueError, TypeError):
        days = 30

    sys.stderr.write(f"[Web] Searching Tavily for: {topic}\n")
    sys.stderr.flush()

    payload = {
        "api_key": api_key,
        "query": topic,
        "max_results": min(count, 20),
        "search_depth": search_depth,
        "exclude_domains": EXCLUDED_DOMAINS,
        "days": days,
    }

    response = http.request(
        "POST",
        ENDPOINT,
        json_data=payload,
        timeout=15,
    )

    return _normalize_results(response, from_date, to_date)


def _normalize_results(
    response: Dict[str, Any],
    from_date: str,
    to_date: str,
) -> List[Dict[str, Any]]:
    """Convert Tavily Search response to websearch item schema."""
    items = []

    raw_results = response.get("results", [])

    for i, result in enumerate(raw_results):
        if not isinstance(result, dict):
            continue

        url = result.get("url", "")
        if not url:
            continue

        # Skip excluded domains (belt and suspenders)
        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                clean_domain = domain[4:]
            else:
                clean_domain = domain
            if clean_domain in ("reddit.com", "twitter.com", "x.com"):
                continue
        except Exception:
            domain = ""
            clean_domain = ""

        title = str(result.get("title", "")).strip()
        snippet = str(result.get("content", "")).strip()

        if not title and not snippet:
            continue

        # Parse date from published_date
        date = None
        date_confidence = "low"
        pub_date = result.get("published_date")
        if pub_date:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', str(pub_date))
            if match:
                date = match.group(1)
                date_confidence = "med"

        # Use Tavily's relevance score
        relevance = result.get("score", 0.6)
        if isinstance(relevance, (int, float)):
            relevance = min(1.0, max(0.0, float(relevance)))
        else:
            relevance = 0.6

        items.append({
            "id": f"W{i+1}",
            "title": title[:200],
            "url": url,
            "source_domain": clean_domain or domain,
            "snippet": snippet[:500],
            "date": date,
            "date_confidence": date_confidence,
            "relevance": relevance,
            "why_relevant": "",
        })

    sys.stderr.write(f"[Web] Tavily: {len(items)} results\n")
    sys.stderr.flush()

    return items

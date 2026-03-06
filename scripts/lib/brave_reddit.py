"""Brave Search-based Reddit thread discovery for last30days skill.

Replaces OpenAI Responses API for Reddit search by using Brave Search
with site:reddit.com filtering. No LLM dependency — results are parsed
directly from Brave's web search results.

The enrichment phase (reddit_enrich.py) still handles engagement data,
top comments, and insights by fetching directly from Reddit's JSON API.
"""

import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse

from . import http
from .brave_search import (
    ENDPOINT,
    _brave_freshness,
    _clean_html,
    _days_between,
    _parse_brave_date,
)

# Noise words to strip from queries for better search precision
_NOISE = {
    'best', 'top', 'latest', 'new', 'trending', 'popular', 'current',
    'tips', 'practices', 'guide', 'tutorial', 'recommendations',
    'using', 'uses', 'use', 'what', 'how', 'is', 'are', 'the',
    'a', 'an', 'for', 'in', 'on', 'of', 'to', 'and', 'or',
}


def _extract_core_subject(topic: str) -> str:
    """Extract core subject from verbose query by removing noise words."""
    words = topic.lower().split()
    result = [w for w in words if w not in _NOISE]
    return ' '.join(result[:5]) or topic.lower().strip()


def _sanitize_query(topic: str) -> str:
    """Strip search operator chars that cause Brave 422 errors."""
    sanitized = re.sub(r'["\':;()\[\]{}\\|&!]', ' ', topic)
    return re.sub(r'\s+', ' ', sanitized).strip()


def search_reddit(
    api_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> List[Dict[str, Any]]:
    """Search for Reddit threads via Brave Search API.

    Args:
        api_key: Brave Search API key
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        List of parsed Reddit item dicts matching the schema expected
        by the enrichment phase.

    Raises:
        http.HTTPError: On API errors
    """
    count = {"quick": 15, "default": 20, "deep": 30}.get(depth, 20)
    days = _days_between(from_date, to_date)
    freshness = _brave_freshness(days)

    query = f"site:reddit.com {_sanitize_query(topic)}"

    params = {
        "q": query,
        "result_filter": "web,news",
        "count": count,
        "safesearch": "strict",
        "text_decorations": 0,
        "spellcheck": 0,
    }
    if freshness:
        params["freshness"] = freshness

    url = f"{ENDPOINT}?{urlencode(params)}"

    sys.stderr.write(f"[Reddit/Brave] Searching: {topic}\n")
    sys.stderr.flush()

    try:
        response = http.request(
            "GET",
            url,
            headers={"X-Subscription-Token": api_key},
            timeout=15,
        )
    except http.HTTPError as e:
        if e.status_code == 422:
            core = _extract_core_subject(topic)
            query = f"site:reddit.com {_sanitize_query(core)}"
            params["q"] = query
            retry_url = f"{ENDPOINT}?{urlencode(params)}"
            response = http.request(
                "GET",
                retry_url,
                headers={"X-Subscription-Token": api_key},
                timeout=15,
            )
        else:
            raise

    items = _parse_results(response)

    sys.stderr.write(f"[Reddit/Brave] Found {len(items)} threads\n")
    sys.stderr.flush()

    # Retry with simplified query if few results
    if len(items) < 5:
        core = _extract_core_subject(topic)
        if core.lower() != topic.lower():
            retry_query = f"site:reddit.com {core}"
            params["q"] = retry_query
            retry_url = f"{ENDPOINT}?{urlencode(params)}"
            try:
                retry_response = http.request(
                    "GET",
                    retry_url,
                    headers={"X-Subscription-Token": api_key},
                    timeout=15,
                )
                retry_items = _parse_results(retry_response)
                existing_urls = {item["url"] for item in items}
                for item in retry_items:
                    if item["url"] not in existing_urls:
                        items.append(item)
            except Exception:
                pass

    # Re-number IDs sequentially
    for i, item in enumerate(items):
        item["id"] = f"R{i + 1}"

    return items


def _parse_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Brave Search response into Reddit item schema."""
    items = []

    raw_results = (
        response.get("news", {}).get("results", []) +
        response.get("web", {}).get("results", [])
    )

    for result in raw_results:
        if not isinstance(result, dict):
            continue

        url = result.get("url", "")
        if not url:
            continue

        # Must be a Reddit thread (not profile, wiki, etc.)
        if not _is_reddit_thread(url):
            continue

        title = _clean_html(str(result.get("title", "")).strip())
        snippet = _clean_html(str(result.get("description", "")).strip())

        if not title:
            continue

        # Extract subreddit from URL
        subreddit = _extract_subreddit(url)

        # Parse date
        date = _parse_brave_date(result.get("age"), result.get("page_age"))
        date_confidence = "med" if date else "low"

        # Clean title — remove "r/subreddit - " prefix and " : subreddit" suffix
        title = re.sub(r'^r/\w+\s*[-–—]\s*', '', title)
        title = re.sub(r'\s*:\s*r/\w+\s*$', '', title)
        title = re.sub(r'\s*[-–—]\s*Reddit\s*$', '', title, flags=re.IGNORECASE)

        items.append({
            "id": "",  # Will be renumbered
            "title": title[:200],
            "url": url,
            "subreddit": subreddit,
            "date": date,
            "date_confidence": date_confidence,
            "engagement": None,
            "top_comments": [],
            "comment_insights": [],
            "relevance": 0.7,
            "why_relevant": snippet[:300] if snippet else "",
            "subs": {
                "relevance": 70,
                "recency": 50,
                "engagement": 50,
            },
            "score": 55,
        })

    # Deduplicate by URL
    seen = set()
    deduped = []
    for item in items:
        if item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)

    return deduped


def _is_reddit_thread(url: str) -> bool:
    """Check if URL is a Reddit thread (not wiki, user profile, etc.)."""
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.lower()
    except Exception:
        return False

    # Must be reddit.com domain
    if not any(host.endswith(d) for d in ('reddit.com',)):
        return False

    # Reject non-community URLs
    if any(sub in host for sub in ('developers.', 'business.', 'mod.')):
        return False

    # Must have /r/ and /comments/ for a thread
    if '/r/' in path and '/comments/' in path:
        return True

    # Also accept /r/subreddit/ posts (some URLs don't have /comments/)
    if '/r/' in path and len(path.split('/')) >= 4:
        return True

    return False


def _extract_subreddit(url: str) -> str:
    """Extract subreddit name from Reddit URL."""
    try:
        path = urlparse(url).path
        parts = [p for p in path.split('/') if p]
        if len(parts) >= 2 and parts[0] == 'r':
            return parts[1]
    except Exception:
        pass
    return ""


def search_subreddits(
    api_key: str,
    subreddits: list,
    topic: str,
    from_date: str,
    to_date: str,
    count_per: int = 5,
) -> list:
    """Search specific subreddits via Brave Search API.

    Replacement for openai_reddit.search_subreddits() which gets 403-blocked
    when hitting Reddit's JSON endpoint directly.

    Args:
        api_key: Brave Search API key
        subreddits: List of subreddit names (without r/)
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        count_per: Results to request per subreddit

    Returns:
        List of raw item dicts matching the schema from parse_reddit_response.
    """
    all_items = []
    core = _extract_core_subject(topic)
    days = _days_between(from_date, to_date)
    freshness = _brave_freshness(days)

    for sub in subreddits:
        sub = sub.lstrip("r/")
        query = f"site:reddit.com/r/{sub} {_sanitize_query(core)}"

        params = {
            "q": query,
            "result_filter": "web,news",
            "count": count_per,
            "safesearch": "strict",
            "text_decorations": 0,
            "spellcheck": 0,
        }
        if freshness:
            params["freshness"] = freshness

        url = f"{ENDPOINT}?{urlencode(params)}"

        try:
            response = http.request(
                "GET",
                url,
                headers={"X-Subscription-Token": api_key},
                timeout=15,
            )
            items = _parse_results(response)
            for item in items:
                item["id"] = f"RS{len(all_items) + 1}"
                item["why_relevant"] = f"Found in r/{sub} supplemental search"
                item["relevance"] = 0.65
            all_items.extend(items)
        except Exception as e:
            sys.stderr.write(f"[Reddit/Brave] Subreddit r/{sub} search failed: {e}\n")
            sys.stderr.flush()

    return all_items

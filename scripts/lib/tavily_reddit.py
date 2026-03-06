"""Tavily-based Reddit thread discovery for last30days skill.

Replaces Brave Search for Reddit discovery by using Tavily Search API
with domain filtering to reddit.com. Results are then enriched with
real engagement data from Reddit's JSON API (reddit_enrich.py).

Tavily API docs: https://docs.tavily.com/
"""

import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from . import http

ENDPOINT = "https://api.tavily.com/search"

# Noise words to strip from queries for better search precision
_NOISE = {
    'best', 'top', 'latest', 'new', 'trending', 'popular', 'current',
    'tips', 'practices', 'guide', 'tutorial', 'recommendations',
    'using', 'uses', 'use', 'what', 'how', 'is', 'are', 'the',
    'a', 'an', 'for', 'in', 'on', 'of', 'to', 'and', 'or',
}

DEPTH_CONFIG = {"quick": 15, "default": 20, "deep": 30}

# Tavily max_results cap is 20 per call
_TAVILY_MAX_PER_CALL = 20


def _extract_core_subject(topic: str) -> str:
    """Extract core subject from verbose query by removing noise words."""
    words = topic.lower().split()
    result = [w for w in words if w not in _NOISE]
    return ' '.join(result[:5]) or topic.lower().strip()


def _sanitize_query(topic: str) -> str:
    """Strip search operator chars that may cause errors."""
    sanitized = re.sub(r'["\':;()\[\]{}\\|&!]', ' ', topic)
    return re.sub(r'\s+', ' ', sanitized).strip()


def _is_reddit_thread(url: str) -> bool:
    """Check if URL is a Reddit thread (not wiki, user profile, etc.)."""
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.lower()
    except Exception:
        return False

    if not any(host.endswith(d) for d in ('reddit.com',)):
        return False

    if any(sub in host for sub in ('developers.', 'business.', 'mod.')):
        return False

    if '/r/' in path and '/comments/' in path:
        return True

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


def _tavily_search(api_key: str, query: str, max_results: int = 20,
                   include_domains: List[str] = None,
                   exclude_domains: List[str] = None,
                   search_depth: str = "basic",
                   days: int = 30) -> Dict[str, Any]:
    """Make a Tavily Search API call.

    Args:
        api_key: Tavily API key
        query: Search query
        max_results: Maximum results (max 20 per call)
        include_domains: Only return results from these domains
        exclude_domains: Exclude results from these domains
        search_depth: 'basic' or 'advanced'
        days: Lookback period in days

    Returns:
        Tavily API response dict
    """
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": min(max_results, _TAVILY_MAX_PER_CALL),
        "search_depth": search_depth,
        "days": days,
    }

    if include_domains:
        payload["include_domains"] = include_domains
    if exclude_domains:
        payload["exclude_domains"] = exclude_domains

    return http.request(
        "POST",
        ENDPOINT,
        json_data=payload,
        timeout=15,
    )


def search_reddit(
    api_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    depth: str = "default",
) -> List[Dict[str, Any]]:
    """Search for Reddit threads via Tavily Search API.

    Args:
        api_key: Tavily API key
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        depth: 'quick', 'default', or 'deep'

    Returns:
        List of parsed Reddit item dicts matching the schema expected
        by the enrichment phase.
    """
    count = DEPTH_CONFIG.get(depth, 20)
    query = _sanitize_query(topic)
    search_depth = "advanced" if depth == "deep" else "basic"

    # Calculate lookback days from dates
    try:
        from datetime import datetime
        d1 = datetime.strptime(from_date, "%Y-%m-%d")
        d2 = datetime.strptime(to_date, "%Y-%m-%d")
        days = max(1, (d2 - d1).days)
    except (ValueError, TypeError):
        days = 30

    sys.stderr.write(f"[Reddit/Tavily] Searching: {topic}\n")
    sys.stderr.flush()

    try:
        response = _tavily_search(
            api_key, query,
            max_results=min(count, _TAVILY_MAX_PER_CALL),
            include_domains=["reddit.com"],
            search_depth=search_depth,
            days=days,
        )
    except http.HTTPError as e:
        if e.status_code in (422, 400):
            # Retry with simplified query
            core = _extract_core_subject(topic)
            query = _sanitize_query(core)
            response = _tavily_search(
                api_key, query,
                max_results=min(count, _TAVILY_MAX_PER_CALL),
                include_domains=["reddit.com"],
                search_depth=search_depth,
                days=days,
            )
        else:
            raise

    items = _parse_results(response)

    # If deep mode needs more than 20, do a second call with refined query
    if count > _TAVILY_MAX_PER_CALL and len(items) >= _TAVILY_MAX_PER_CALL - 2:
        existing_urls = {item["url"] for item in items}
        core = _extract_core_subject(topic)
        if core.lower() != topic.lower():
            try:
                response2 = _tavily_search(
                    api_key, _sanitize_query(core),
                    max_results=_TAVILY_MAX_PER_CALL,
                    include_domains=["reddit.com"],
                    search_depth=search_depth,
                    days=days,
                )
                for item in _parse_results(response2):
                    if item["url"] not in existing_urls:
                        items.append(item)
                        existing_urls.add(item["url"])
            except Exception:
                pass

    sys.stderr.write(f"[Reddit/Tavily] Found {len(items)} threads\n")
    sys.stderr.flush()

    # Retry with simplified query if few results
    if len(items) < 5:
        core = _extract_core_subject(topic)
        if core.lower() != topic.lower():
            try:
                retry_response = _tavily_search(
                    api_key, _sanitize_query(core),
                    max_results=_TAVILY_MAX_PER_CALL,
                    include_domains=["reddit.com"],
                    search_depth=search_depth,
                    days=days,
                )
                existing_urls = {item["url"] for item in items}
                for item in _parse_results(retry_response):
                    if item["url"] not in existing_urls:
                        items.append(item)
            except Exception:
                pass

    # Re-number IDs sequentially
    for i, item in enumerate(items):
        item["id"] = f"R{i + 1}"

    return items


def _parse_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Tavily Search response into Reddit item schema."""
    items = []

    raw_results = response.get("results", [])

    for result in raw_results:
        if not isinstance(result, dict):
            continue

        url = result.get("url", "")
        if not url:
            continue

        if not _is_reddit_thread(url):
            continue

        title = str(result.get("title", "")).strip()
        snippet = str(result.get("content", "")).strip()

        if not title:
            continue

        subreddit = _extract_subreddit(url)

        # Parse date from published_date if available
        date = None
        date_confidence = "low"
        pub_date = result.get("published_date")
        if pub_date:
            # Tavily returns ISO dates like "2026-02-15T..."
            match = re.search(r'(\d{4}-\d{2}-\d{2})', str(pub_date))
            if match:
                date = match.group(1)
                date_confidence = "high"

        # Clean title — remove "r/subreddit - " prefix and " : subreddit" suffix
        title = re.sub(r'^r/\w+\s*[-–—]\s*', '', title)
        title = re.sub(r'\s*:\s*r/\w+\s*$', '', title)
        title = re.sub(r'\s*[-–—]\s*Reddit\s*$', '', title, flags=re.IGNORECASE)

        # Use Tavily's relevance score if available
        relevance = result.get("score", 0.7)
        if isinstance(relevance, (int, float)):
            relevance = min(1.0, max(0.0, float(relevance)))
        else:
            relevance = 0.7

        items.append({
            "id": "",
            "title": title[:200],
            "url": url,
            "subreddit": subreddit,
            "date": date,
            "date_confidence": date_confidence,
            "engagement": None,
            "top_comments": [],
            "comment_insights": [],
            "relevance": relevance,
            "why_relevant": snippet[:300] if snippet else "",
            "subs": {
                "relevance": int(relevance * 100),
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


def search_subreddits(
    api_key: str,
    subreddits: list,
    topic: str,
    from_date: str,
    to_date: str,
    count_per: int = 5,
) -> list:
    """Search specific subreddits via Tavily Search API.

    Args:
        api_key: Tavily API key
        subreddits: List of subreddit names (without r/)
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        count_per: Results to request per subreddit

    Returns:
        List of raw item dicts.
    """
    all_items = []
    core = _extract_core_subject(topic)

    try:
        from datetime import datetime
        d1 = datetime.strptime(from_date, "%Y-%m-%d")
        d2 = datetime.strptime(to_date, "%Y-%m-%d")
        days = max(1, (d2 - d1).days)
    except (ValueError, TypeError):
        days = 30

    for sub in subreddits:
        sub = sub.lstrip("r/")
        query = f"site:reddit.com/r/{sub} {_sanitize_query(core)}"

        try:
            response = _tavily_search(
                api_key, query,
                max_results=min(count_per, _TAVILY_MAX_PER_CALL),
                include_domains=[f"reddit.com"],
                search_depth="basic",
                days=days,
            )
            items = _parse_results(response)
            for item in items:
                item["id"] = f"RS{len(all_items) + 1}"
                item["why_relevant"] = f"Found in r/{sub} supplemental search"
                item["relevance"] = 0.65
            all_items.extend(items)
        except Exception as e:
            sys.stderr.write(f"[Reddit/Tavily] Subreddit r/{sub} search failed: {e}\n")
            sys.stderr.flush()

    return all_items

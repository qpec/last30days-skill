"""Podcast episode discovery and transcript enrichment for last30days skill.

Two-phase approach:
  Phase 1 (Discovery): Use Tavily with podcast domain filtering to find episodes
  Phase 2 (Enrichment): Use Listen Notes API for transcript enrichment (if key available)
"""

import re
import sys
import time
from typing import Any, Dict, List, Optional

from . import http

# Tavily endpoint
TAVILY_ENDPOINT = "https://api.tavily.com/search"

# Listen Notes API
LISTEN_NOTES_ENDPOINT = "https://listen-api.listennotes.com/api/v2"

# Podcast discovery domains for Tavily
PODCAST_DOMAINS = [
    "podcasts.apple.com",
    "open.spotify.com",
    "podcasts.google.com",
    "pca.st",
    "listennotes.com",
    "podcastaddict.com",
    "overcast.fm",
]

DEPTH_CONFIG = {"quick": 8, "default": 15, "deep": 25}


def _log(msg: str):
    """Log to stderr."""
    sys.stderr.write(f"[Podcast] {msg}\n")
    sys.stderr.flush()


def search_podcasts(
    topic: str,
    from_date: str,
    to_date: str,
    tavily_key: str,
    listen_notes_key: Optional[str] = None,
    depth: str = "default",
) -> List[Dict[str, Any]]:
    """Search for podcast episodes.

    Phase 1: Tavily domain-filtered search for podcast content
    Phase 2: Listen Notes transcript enrichment (if key available)

    Args:
        topic: Search topic
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        tavily_key: Tavily API key (required for discovery)
        listen_notes_key: Listen Notes API key (optional, for transcripts)
        depth: 'quick', 'default', or 'deep'

    Returns:
        List of podcast item dicts
    """
    max_results = DEPTH_CONFIG.get(depth, 15)

    # Phase 1: Discover via Tavily
    _log(f"Searching for podcast episodes: {topic}")
    episodes = _search_via_tavily(tavily_key, topic, from_date, to_date, max_results)

    # Phase 2: Enrich via Listen Notes (if key available)
    if listen_notes_key and episodes:
        _log(f"Enriching {len(episodes)} episodes via Listen Notes")
        episodes = _enrich_via_listen_notes(listen_notes_key, episodes, topic)

    # Also search Listen Notes directly for additional results
    if listen_notes_key:
        ln_episodes = _search_listen_notes(listen_notes_key, topic, from_date, to_date, max_results)
        existing_titles = {ep.get("title", "").lower() for ep in episodes}
        for ep in ln_episodes:
            if ep.get("title", "").lower() not in existing_titles:
                episodes.append(ep)
                existing_titles.add(ep.get("title", "").lower())

    # Assign IDs
    for i, ep in enumerate(episodes):
        ep["id"] = f"P{i + 1}"

    _log(f"Found {len(episodes)} podcast episodes total")
    return episodes


def _search_via_tavily(
    tavily_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    max_results: int,
) -> List[Dict[str, Any]]:
    """Discover podcast episodes via Tavily with domain filtering."""
    try:
        from datetime import datetime
        d1 = datetime.strptime(from_date, "%Y-%m-%d")
        d2 = datetime.strptime(to_date, "%Y-%m-%d")
        days = max(1, (d2 - d1).days)
    except (ValueError, TypeError):
        days = 30

    query = f"{topic} podcast episode"

    payload = {
        "api_key": tavily_key,
        "query": query,
        "max_results": min(max_results, 20),
        "search_depth": "basic",
        "include_domains": PODCAST_DOMAINS,
        "days": days,
    }

    try:
        response = http.request(
            "POST",
            TAVILY_ENDPOINT,
            json_data=payload,
            timeout=15,
        )
    except Exception as e:
        _log(f"Tavily podcast search failed: {e}")
        return []

    return _parse_tavily_podcast_results(response)


def _parse_tavily_podcast_results(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse Tavily results into podcast episode format."""
    episodes = []

    for result in response.get("results", []):
        if not isinstance(result, dict):
            continue

        url = result.get("url", "")
        title = str(result.get("title", "")).strip()
        content = str(result.get("content", "")).strip()

        if not url or not title:
            continue

        # Try to parse podcast name and episode title from the title
        podcast_name, episode_title = _parse_podcast_title(title, url)

        # Parse date
        date = None
        date_confidence = "low"
        pub_date = result.get("published_date")
        if pub_date:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', str(pub_date))
            if match:
                date = match.group(1)
                date_confidence = "med"

        relevance = result.get("score", 0.6)
        if isinstance(relevance, (int, float)):
            relevance = min(1.0, max(0.0, float(relevance)))
        else:
            relevance = 0.6

        episodes.append({
            "id": "",
            "title": title[:200],
            "url": url,
            "podcast_name": podcast_name,
            "episode_title": episode_title,
            "date": date,
            "date_confidence": date_confidence,
            "engagement": None,
            "transcript_snippet": content[:500] if content else "",
            "transcript_full": "",
            "relevance": relevance,
            "why_relevant": f"Podcast episode about {title[:100]}",
        })

    return episodes


def _parse_podcast_title(title: str, url: str) -> tuple:
    """Try to extract podcast name and episode title from combined title.

    Returns:
        Tuple of (podcast_name, episode_title)
    """
    # Common separators: " - ", " | ", " : "
    for sep in [" - ", " | ", " : ", " — ", " – "]:
        if sep in title:
            parts = title.split(sep, 1)
            return parts[0].strip(), parts[1].strip()

    # Try to get podcast name from URL
    if "podcasts.apple.com" in url:
        return "Apple Podcasts", title
    elif "open.spotify.com" in url:
        return "Spotify", title
    elif "listennotes.com" in url:
        return "Listen Notes", title

    return "", title


def _enrich_via_listen_notes(
    listen_notes_key: str,
    episodes: List[Dict[str, Any]],
    topic: str,
) -> List[Dict[str, Any]]:
    """Enrich episodes with Listen Notes data (transcripts, metadata)."""
    for episode in episodes:
        try:
            title = episode.get("episode_title") or episode.get("title", "")
            if not title:
                continue

            # Search Listen Notes for this specific episode
            search_url = f"{LISTEN_NOTES_ENDPOINT}/search?q={_url_encode(title)}&type=episode&sort_by_date=1&len_min=5"
            response = http.request(
                "GET",
                search_url,
                headers={"X-ListenAPI-Key": listen_notes_key},
                timeout=10,
                retries=1,
            )

            results = response.get("results", [])
            if results:
                best = results[0]
                # Update with Listen Notes data
                if best.get("podcast", {}).get("title"):
                    episode["podcast_name"] = best["podcast"]["title"]
                if best.get("title_original"):
                    episode["episode_title"] = best["title_original"]
                if best.get("pub_date_ms"):
                    from datetime import datetime
                    try:
                        dt = datetime.fromtimestamp(best["pub_date_ms"] / 1000)
                        episode["date"] = dt.strftime("%Y-%m-%d")
                        episode["date_confidence"] = "high"
                    except (ValueError, OSError):
                        pass
                if best.get("listennotes_url"):
                    episode["url"] = best["listennotes_url"]
                if best.get("description_highlighted") or best.get("description_original"):
                    desc = best.get("description_original", best.get("description_highlighted", ""))
                    # Strip HTML
                    desc = re.sub(r'<[^>]+>', '', desc)
                    if desc and len(desc) > len(episode.get("transcript_snippet", "")):
                        episode["transcript_snippet"] = desc[:500]

            time.sleep(0.3)  # Rate limit courtesy
        except Exception as e:
            _log(f"Listen Notes enrichment failed for '{episode.get('title', '')[:50]}': {e}")

    return episodes


def _search_listen_notes(
    listen_notes_key: str,
    topic: str,
    from_date: str,
    to_date: str,
    max_results: int,
) -> List[Dict[str, Any]]:
    """Direct Listen Notes search for podcast episodes."""
    try:
        from datetime import datetime
        published_after = int(datetime.strptime(from_date, "%Y-%m-%d").timestamp())
    except (ValueError, TypeError):
        published_after = None

    search_url = f"{LISTEN_NOTES_ENDPOINT}/search?q={_url_encode(topic)}&type=episode&sort_by_date=1&len_min=5"
    if published_after:
        search_url += f"&published_after={published_after}"

    try:
        response = http.request(
            "GET",
            search_url,
            headers={"X-ListenAPI-Key": listen_notes_key},
            timeout=15,
            retries=2,
        )
    except Exception as e:
        _log(f"Listen Notes search failed: {e}")
        return []

    episodes = []
    for result in response.get("results", [])[:max_results]:
        if not isinstance(result, dict):
            continue

        podcast_title = result.get("podcast", {}).get("title", "")
        episode_title = result.get("title_original", "")
        url = result.get("listennotes_url", "")

        if not episode_title or not url:
            continue

        # Parse date
        date = None
        date_confidence = "low"
        if result.get("pub_date_ms"):
            try:
                from datetime import datetime
                dt = datetime.fromtimestamp(result["pub_date_ms"] / 1000)
                date = dt.strftime("%Y-%m-%d")
                date_confidence = "high"
            except (ValueError, OSError):
                pass

        # Get description as transcript snippet
        desc = result.get("description_original", "")
        desc = re.sub(r'<[^>]+>', '', desc)

        episodes.append({
            "id": "",
            "title": f"{podcast_title} - {episode_title}"[:200],
            "url": url,
            "podcast_name": podcast_title,
            "episode_title": episode_title,
            "date": date,
            "date_confidence": date_confidence,
            "engagement": None,
            "transcript_snippet": desc[:500],
            "transcript_full": "",
            "relevance": 0.65,
            "why_relevant": f"Podcast episode from Listen Notes about {topic[:50]}",
        })

    _log(f"Listen Notes: {len(episodes)} episodes found")
    return episodes


def _url_encode(text: str) -> str:
    """URL-encode a string."""
    from urllib.parse import quote
    return quote(text, safe='')

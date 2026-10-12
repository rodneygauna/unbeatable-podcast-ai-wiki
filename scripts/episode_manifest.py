#!/usr/bin/env python3
"""
Episode Manifest Script

This script handles the creation and management of episode manifests for
the Unbeatable Podcast AI Wiki. Using the yt-dlp tool, it will:
1. Download episode metadata from the UnbeatableCast YouTube channel.
2. Generate and update an episode manifest (JSON).

Each run lists the channel, fetches full metadata only for episodes not yet in
the manifest, and refreshes lightweight fields (title, availability) for
known ones. Use --refresh to re-fetch full metadata for every episode.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp is required: pip install -r requirements.txt")

CHANNEL_URL = "https://www.youtube.com/@UnbeatableCast"
DEFAULT_TABS = ["videos"]
DEFAULT_OUTPUT = Path(__file__).resolve(
).parent.parent / "data" / "episodes.json"
MANIFEST_VERSION = 1

# e.g. "Pokémon Tabletop - Poké Party - 15 - Unbeatable: Road to Victory"
#      "Welcome to the World of Pokemon - 01- Unbeatable: A Kanto Journey"
TITLE_PATTERN = re.compile(
    r"^(?:(?P<prefix>.+?)\s*-\s*)?(?P<name>.+?)\s*-\s*"
    r"(?P<number>\d+(?:\.\d+)?)\s*-\s*(?P<series>.+)$"
)

log = logging.getLogger("episode_manifest")


def now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def iso_date(yyyymmdd: str | None) -> str | None:
    """Convert YYYYMMDD string to YYYY-MM-DD format."""
    if not yyyymmdd or len(yyyymmdd) != 8:
        return None
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"


def parse_title(title: str | None) -> dict[str, Any]:
    """Best-effort extraction of series and episode number from the title."""
    match = TITLE_PATTERN.match(title or "")
    if not match:
        return {"series": None, "episode_number": None, "episode_name": None}
    number = match["number"]
    return {
        "series": match["series"].strip(),
        "episode_number": float(number) if "." in number else int(number),
        "episode_name": match["name"].strip(),
    }


def ydl_options(**extra: Any) -> dict[str, Any]:
    """Return default yt-dlp configuration options."""
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "ignoreerrors": False,
    }
    opts.update(extra)
    return opts


def list_channel_videos(
    channel_url: str, tabs: list[str]
) -> list[dict[str, Any]]:
    """Return flat (cheap) entries for videos in the given channel tabs."""
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    with yt_dlp.YoutubeDL(ydl_options(extract_flat="in_playlist")) as ydl:
        for tab in tabs:
            url = f"{channel_url.rstrip('/')}/{tab}"
            log.info("Listing %s", url)
            info = ydl.extract_info(url, download=False) or {}
            for entry in info.get("entries") or []:
                if not entry or not entry.get("id") or entry["id"] in seen:
                    continue
                seen.add(entry["id"])
                entry["_source_tab"] = tab
                entries.append(entry)
    log.info("Found %d videos on channel", len(entries))
    return entries


def fetch_full_metadata(
    ydl: yt_dlp.YoutubeDL, video_id: str
) -> dict[str, Any] | None:
    """Fetch and sanitize full video metadata using yt-dlp."""
    try:
        info = ydl.extract_info(
            f"https://www.youtube.com/watch?v={video_id}", download=False
        )
    except yt_dlp.utils.DownloadError as exc:
        log.warning("Could not fetch %s: %s", video_id, exc)
        return None
    return ydl.sanitize_info(info) if info else None


def build_episode(info: dict[str, Any], source_tab: str) -> dict[str, Any]:
    """Construct a normalized episode dict from yt-dlp info."""
    url = (
        info.get("webpage_url")
        or f"https://www.youtube.com/watch?v={info['id']}"
    )
    return {
        "id": info["id"],
        "title": info.get("title"),
        **parse_title(info.get("title")),
        "url": url,
        "upload_date": iso_date(info.get("upload_date")),
        "timestamp": info.get("timestamp"),
        "duration": info.get("duration"),
        "duration_string": info.get("duration_string"),
        "description": info.get("description"),
        "availability": info.get("availability"),
        "source_tab": source_tab,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    """Load existing manifest JSON or return an empty structure."""
    if not path.exists():
        return {"episodes": []}
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Write atomically so an interrupted run never corrupts the manifest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def sort_key(ep: dict[str, Any]) -> tuple:
    """Sorting key tuple for chronological ordering."""
    return (ep.get("timestamp") or 0, ep.get("upload_date") or "", ep["id"])


def build_manifest(
    episodes: dict[str, dict[str, Any]], channel_url: str, tabs: list[str]
) -> dict[str, Any]:
    """Build top-level manifest dictionary."""
    ordered = sorted(episodes.values(), key=sort_key)
    return {
        "manifest_version": MANIFEST_VERSION,
        "channel_url": channel_url,
        "tabs": tabs,
        "last_updated": now_iso(),
        "episode_count": len(ordered),
        "episodes": ordered,
    }


def update_manifest(
    output: Path,
    channel_url: str,
    tabs: list[str],
    refresh: bool = False,
    limit: int | None = None,
    checkpoint_every: int = 10,
) -> dict[str, int]:
    """Fetch video metadata from channel and update local manifest file."""
    manifest = load_manifest(output)
    episodes: dict[str, dict[str, Any]] = {
        e["id"]: e for e in manifest.get("episodes", [])}
    stats = {"added": 0, "refreshed": 0,
             "updated": 0, "missing": 0, "failed": 0}
    timestamp = now_iso()

    listing = list_channel_videos(channel_url, tabs)
    listed_ids = {e["id"] for e in listing}

    to_fetch = [e for e in listing if refresh or e["id"] not in episodes]
    if limit is not None:
        to_fetch = to_fetch[:limit]
    fetch_ids = {e["id"] for e in to_fetch}

    # Cheap update for known episodes from the flat listing.
    for entry in listing:
        ep = episodes.get(entry["id"])
        if ep is None or entry["id"] in fetch_ids:
            continue
        changed = False
        for key in ("title", "availability"):
            value = entry.get(key)
            if value is not None and ep.get(key) != value:
                ep[key] = value
                changed = True
        if changed:
            ep["metadata_updated_at"] = timestamp
            stats["updated"] += 1
        ep.pop("missing_since", None)

    # Re-derive parsed fields so parser improvements apply to existing entries.
    for ep in episodes.values():
        ep.update(parse_title(ep.get("title")))

    # Keep episodes that vanished from the channel, but flag them.
    for vid, ep in episodes.items():
        if vid not in listed_ids and "missing_since" not in ep:
            ep["missing_since"] = timestamp
            stats["missing"] += 1

    log.info("Fetching full metadata for %d video(s)", len(to_fetch))
    with yt_dlp.YoutubeDL(ydl_options()) as ydl:
        for index, entry in enumerate(to_fetch, start=1):
            vid = entry["id"]
            log.info("[%d/%d] %s %s", index, len(to_fetch),
                     vid, entry.get("title", ""))
            info = fetch_full_metadata(ydl, vid)
            if info is None:
                stats["failed"] += 1
                continue
            existing = episodes.get(vid)
            episode = build_episode(info, entry["_source_tab"])
            episode["first_seen_at"] = existing.get(
                "first_seen_at", timestamp) if existing else timestamp
            episode["metadata_updated_at"] = timestamp
            if existing and "directory" in existing:
                episode["directory"] = existing["directory"]
            episodes[vid] = episode
            stats["refreshed" if existing else "added"] += 1

            if checkpoint_every and index % checkpoint_every == 0:
                save_manifest(output, build_manifest(
                    episodes, channel_url, tabs))

    save_manifest(output, build_manifest(episodes, channel_url, tabs))
    return stats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"Manifest JSON path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--channel", default=CHANNEL_URL,
                        help=f"Channel URL (default: {CHANNEL_URL})")
    parser.add_argument(
        "--tabs",
        nargs="+",
        default=DEFAULT_TABS,
        help="Channel tabs to scan, e.g. videos streams shorts "
             "(default: videos)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-fetch full metadata for all episodes, not just new ones",
    )
    parser.add_argument("--limit", type=int,
                        help="Max number of videos to fully fetch this run")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="Debug logging")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for updating episode manifest."""
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        stats = update_manifest(args.output, args.channel,
                                args.tabs, args.refresh, args.limit)
    except yt_dlp.utils.DownloadError as exc:
        log.error("Failed to list channel: %s", exc)
        return 1
    log.info(
        "Done: %d added, %d refreshed, %d updated, %d newly missing, "
        "%d failed -> %s",
        stats["added"],
        stats["refreshed"],
        stats["updated"],
        stats["missing"],
        stats["failed"],
        args.output,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

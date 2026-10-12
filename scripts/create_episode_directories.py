#!/usr/bin/env python3
"""
Create Episode Directories Script

This script creates a chronological directory for each episode listed in
data/episodes.json (e.g., episodes/001-slug/) containing a .gitkeep file, and
updates the manifest with the directory path to ensure idempotent runs.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "data" / "episodes.json"
DEFAULT_BASE_DIR = REPO_ROOT / "episodes"

log = logging.getLogger("create_episode_directories")


def slugify(text: str, max_len: int = 50) -> str:
    """Normalize text to ASCII, convert non-alphanumeric chars to hyphens."""
    normalized = unicodedata.normalize("NFKD", text).encode(
        "ascii", "ignore"
    ).decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")
    if not slug:
        return "episode"
    if len(slug) > max_len:
        truncated = slug[:max_len].rsplit("-", 1)[0]
        slug = truncated if truncated else slug[:max_len]
    return slug.strip("-")


def load_manifest(path: Path) -> dict[str, Any]:
    """Load JSON manifest from file path."""
    if not path.is_file():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Save manifest atomically using a temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", dir=path.parent, delete=False, encoding="utf-8"
        ) as fh:
            tmp = fh.name
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if tmp:
            Path(tmp).unlink(missing_ok=True)
        raise


def get_relative_dir_path(target_path: Path, reference_dir: Path) -> str:
    """Return relative POSIX path from reference_dir or target_path name."""
    try:
        rel = target_path.resolve().relative_to(reference_dir.resolve())
        return rel.as_posix()
    except ValueError:
        return target_path.as_posix()


def process_episodes(
    manifest_path: Path,
    base_dir: Path,
    dry_run: bool = False,
    gitkeep: bool = True,
) -> dict[str, int]:
    """Create episode directories and update manifest idempotently."""
    manifest = load_manifest(manifest_path)
    episodes: list[dict[str, Any]] = manifest.get("episodes", [])

    stats = {
        "total": len(episodes),
        "existing_skipped": 0,
        "restored_dirs": 0,
        "created_dirs": 0,
        "manifest_updated": 0,
    }

    # Find highest existing chronological index in assigned directories
    max_index = 0
    for ep in episodes:
        dir_val = ep.get("directory")
        if dir_val:
            folder_name = Path(dir_val).name
            m = re.match(r"^(\d+)-", folder_name)
            if m:
                max_index = max(max_index, int(m.group(1)))

    manifest_changed = False
    current_index = max_index

    # If no directories were assigned, index will be 1-based sequential
    assign_sequential = max_index == 0

    for idx, ep in enumerate(episodes, start=1):
        vid = ep.get("id", "unknown")
        title = ep.get("title") or vid
        existing_dir = ep.get("directory")

        if existing_dir:
            target_dir = REPO_ROOT / existing_dir
            if target_dir.is_dir():
                stats["existing_skipped"] += 1
                log.debug(
                    "Skipping existing directory for %s: %s", vid, existing_dir
                )
                continue

            # Directory in manifest but missing on disk; recreate it
            stats["restored_dirs"] += 1
            log.info(
                "Restoring missing directory for %s: %s", vid, target_dir
            )
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                if gitkeep:
                    gitkeep_path = target_dir / ".gitkeep"
                    if not gitkeep_path.exists():
                        gitkeep_path.touch()
            continue

        # Episode does not have a directory assigned yet
        if assign_sequential:
            ep_index = idx
        else:
            current_index += 1
            ep_index = current_index

        folder_name = f"{ep_index:03d}-{slugify(title)}"
        target_dir = base_dir / folder_name
        rel_dir = get_relative_dir_path(target_dir, REPO_ROOT)

        stats["created_dirs"] += 1
        log.info("Creating directory for [%d] %s: %s", ep_index, vid, rel_dir)

        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            if gitkeep:
                gitkeep_path = target_dir / ".gitkeep"
                if not gitkeep_path.exists():
                    gitkeep_path.touch()

            ep["directory"] = rel_dir
            manifest_changed = True
            stats["manifest_updated"] += 1
        else:
            stats["manifest_updated"] += 1

    if manifest_changed and not dry_run:
        save_manifest(manifest_path, manifest)
        log.info("Updated manifest saved to %s", manifest_path)

    return stats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-m",
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"Manifest JSON path (default: {DEFAULT_MANIFEST})",
    )
    parser.add_argument(
        "-b",
        "--base-dir",
        type=Path,
        default=DEFAULT_BASE_DIR,
        help="Base directory for episode folders "
             f"(default: {DEFAULT_BASE_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate execution without creating directories or "
             "saving the manifest",
    )
    parser.add_argument(
        "--no-gitkeep",
        action="store_true",
        help="Do not create .gitkeep files in newly created directories",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable debug logging"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Main entry point for creating episode directories."""
    args = parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    try:
        stats = process_episodes(
            manifest_path=args.manifest,
            base_dir=args.base_dir,
            dry_run=args.dry_run,
            gitkeep=not args.no_gitkeep,
        )
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        log.error("Execution failed: %s", exc)
        return 1

    log.info(
        "Done. Total episodes: %d, created: %d, restored: %d, "
        "skipped: %d, manifest entries updated: %d",
        stats["total"],
        stats["created_dirs"],
        stats["restored_dirs"],
        stats["existing_skipped"],
        stats["manifest_updated"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

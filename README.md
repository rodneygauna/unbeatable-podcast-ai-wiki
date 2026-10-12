# unbeatable-podcast-ai-wiki

## Episode manifest

`scripts/episode_manifest.py` uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to collect episode metadata from the [UnbeatableCast YouTube channel](https://www.youtube.com/@UnbeatableCast) into `data/episodes.json`.

```bash
pip install -r requirements.txt
python3 scripts/episode_manifest.py
```

Re-running the script updates the manifest: full metadata is fetched only for new videos, titles/status of known videos are synced, and videos removed from the channel are kept but marked with `missing_since`.

Options:

- `--refresh` – re-fetch full metadata (description, duration, etc.) for every episode
- `--tabs videos streams shorts` – channel tabs to scan (default: `videos`)
- `--limit N` – fetch at most N videos this run
- `-o PATH` – write the manifest somewhere else

### Manifest format

Top-level keys: `manifest_version`, `channel_url`, `tabs`, `last_updated`, `episode_count`, and `episodes` (sorted oldest to newest).

Each episode contains:

| Field | Description |
| --- | --- |
| `id` | YouTube video ID |
| `title` | Video title |
| `series` | Series name parsed from the title (e.g. `Unbeatable: Road to Victory`), or `null` |
| `episode_number` | Episode number parsed from the title (may be a decimal such as `9.5`), or `null` |
| `episode_name` | Episode name parsed from the title, or `null` |
| `url` | Video URL |
| `upload_date` | Upload date (`YYYY-MM-DD`) |
| `timestamp` | Upload time as a Unix timestamp |
| `duration` | Length in seconds |
| `duration_string` | Length formatted as `H:MM:SS` |
| `description` | Video description |
| `availability` | e.g. `public`, `unlisted` |
| `source_tab` | Channel tab the video was found on |
| `first_seen_at` | When the script first added the video (UTC) |
| `metadata_updated_at` | When the entry was last updated (UTC) |
| `directory` | Relative path to the episode directory (e.g. `episodes/001-...`) |
| `missing_since` | Only present if the video is no longer listed on the channel |

## Episode directories

`scripts/create_episode_directories.py` creates a dedicated directory for each episode in chronological order under `episodes/` (e.g. `episodes/001-slug/`), places a `.gitkeep` inside so Git tracks the directory, and records the directory path back into `data/episodes.json`.

```bash
python3 scripts/create_episode_directories.py
```

Re-running the script is safe and idempotent: it skips episodes that already have existing directories and only creates directories for new episodes or restores missing ones.

Options:

- `--dry-run` – preview directory creations and manifest changes without writing to disk
- `-b PATH`, `--base-dir PATH` – target base directory for episode folders (default: `episodes`)
- `-m PATH`, `--manifest PATH` – manifest JSON path (default: `data/episodes.json`)
- `--no-gitkeep` – skip adding `.gitkeep` files in created directories
- `-v`, `--verbose` – enable debug logging


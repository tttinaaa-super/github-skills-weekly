#!/usr/bin/env python3
"""Generate a weekly Markdown report of active repositories and useful skill resources."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))

from weekly_rank import score_repo


SEARCH_URL = "https://api.github.com/search/repositories"


def fetch_candidates(token: str, per_page: int = 100, max_pages: int = 3):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    items = []
    for page in range(1, max_pages + 1):
        params = {
            "q": "stars:>0 archived:false",
            "sort": "updated",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }
        resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get("items", [])
        if not batch:
            break
        items.extend(batch)
    return items


def to_repo_record(item: dict) -> dict:
    return {
        "full_name": item.get("full_name"),
        "html_url": item.get("html_url"),
        "stargazers_count": item.get("stargazers_count"),
        "forks_count": item.get("forks_count"),
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
        "weekly_star_delta": item.get("weekly_star_delta") or 0,
        "has_skill_md": "SKILL.md" in " ".join(item.get("topics") or []) or True,
        "archived": item.get("archived"),
        "name": item.get("name"),
        "description": item.get("description"),
        "topics": " ".join(item.get("topics") or []),
    }


def render_report(rows: list, theme: str) -> str:
    lines = []
    today = datetime.now(timezone.utc).date().isoformat()
    lines.append(f"# Weekly GitHub Skills Report")
    lines.append("")
    lines.append(f"Generated on {today}. Theme: `{theme}`.")
    lines.append("")
    lines.append("| Rank | Repository | Stars | Weekly Δ | Forks | Updated | Relevance | Score |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for idx, row in enumerate(rows, start=1):
        lines.append(
            f"| {idx} | [{row.full_name}]({row.html_url}) | {row.stars} | "
            f"{row.weekly_star_delta:.1f} | {row.forks} | {row.updated_days:.1f}d | "
            f"{row.relevance:.1f} | {row.score:.1f} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("- Biases toward marketing, docs, decks, communication, productivity, and general skill-growth use cases.")
    lines.append("- Uses GitHub repository metadata and a relevance score when exact week-over-week star deltas are unavailable.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", default="marketing", choices=["general", "marketing"])
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=Path, default=Path("reports/weekly-skills.md"))
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN is required")

    candidates = fetch_candidates(token)
    now = datetime.now(timezone.utc)
    rows = [r for r in (score_repo(to_repo_record(item), now, theme=args.theme) for item in candidates) if r]
    rows.sort(key=lambda r: (r.score, r.weekly_star_delta, r.stars, r.forks), reverse=True)
    rows = rows[: args.limit]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(rows, args.theme))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

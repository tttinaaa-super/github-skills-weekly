#!/usr/bin/env python3
"""Rank GitHub repositories that contain SKILL.md files.

Input: a JSON array of repository objects on stdin or from --input.
Each object may contain:
- full_name
- html_url
- stargazers_count
- fork_count or forks_count
- updated_at
- pushed_at
- weekly_star_delta
- has_skill_md
- archived

The script emits a Markdown leaderboard and a compact score breakdown.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def days_since(ts: str | None, now: datetime) -> float | None:
    dt = parse_iso(ts)
    if not dt:
        return None
    return max((now - dt).total_seconds() / 86400.0, 0.0)


@dataclass
class RepoRow:
    full_name: str
    html_url: str
    stars: int
    forks: int
    weekly_star_delta: float
    updated_days: float
    pushed_days: float
    score: float
    relevance: float
    tags: str


MARKETING_KEYWORDS = (
    "brand",
    "deck",
    "doc",
    "docs",
    "presentation",
    "pdf",
    "slack",
    "communication",
    "comms",
    "marketing",
    "productivity",
    "workflow",
    "writing",
    "spreadsheet",
    "xlsx",
    "theme",
    "design",
    "canvas",
)

CODING_KEYWORDS = (
    "cli",
    "sdk",
    "framework",
    "compiler",
    "lint",
    "debug",
    "dev",
    "server",
    "api",
    "backend",
    "frontend",
    "typescript",
    "python",
    "javascript",
    "go",
    "rust",
)


def keyword_score(text: str, keywords: tuple[str, ...]) -> float:
    lowered = (text or "").lower()
    return sum(1.0 for kw in keywords if kw in lowered)


def score_repo(repo: dict, now: datetime, theme: str = "general") -> RepoRow | None:
    if repo.get("archived") or not repo.get("has_skill_md", True):
        return None

    full_name = repo.get("full_name") or repo.get("name")
    if not full_name:
        return None

    text = " ".join(
        str(repo.get(field) or "")
        for field in ("name", "full_name", "description", "topics")
    )
    relevance = keyword_score(text, MARKETING_KEYWORDS) - keyword_score(text, CODING_KEYWORDS) * 0.7
    if theme == "marketing":
        relevance = max(relevance, 0.0)

    topic_text = text.lower()
    tags = []
    if any(keyword in topic_text for keyword in ("brand", "deck", "doc", "docs", "presentation", "pdf", "slack", "communication", "comms", "marketing")):
        tags.append("marketing")
    if any(keyword in topic_text for keyword in ("productivity", "workflow", "spreadsheet", "xlsx", "template", "automation", "efficiency")):
        tags.append("productivity")
    if any(keyword in topic_text for keyword in ("learn", "lesson", "course", "study", "growth", "writing", "practice", "skill")):
        tags.append("skill-growth")
    if not tags:
        tags.append("general")

    stars = int(repo.get("stargazers_count") or 0)
    forks = int(repo.get("fork_count") or repo.get("forks_count") or 0)
    weekly_star_delta = float(repo.get("weekly_star_delta") or 0.0)
    updated_days = days_since(repo.get("updated_at"), now) or 999.0
    pushed_days = days_since(repo.get("pushed_at"), now) or 999.0

    freshness = max(0.0, 30.0 - updated_days) / 30.0
    push_freshness = max(0.0, 14.0 - pushed_days) / 14.0
    star_component = min(stars, 5000) / 5000.0
    fork_component = min(forks, 1000) / 1000.0

    score = (
        weekly_star_delta * 6.0
        + freshness * 25.0
        + push_freshness * 15.0
        + star_component * 20.0
        + fork_component * 10.0
        + relevance * 8.0
    )

    return RepoRow(
        full_name=full_name,
        html_url=repo.get("html_url") or "",
        stars=stars,
        forks=forks,
        weekly_star_delta=weekly_star_delta,
        updated_days=updated_days,
        pushed_days=pushed_days,
        score=score,
        relevance=relevance,
        tags=", ".join(tags),
    )


def render(rows: list[RepoRow]) -> str:
    lines = []
    lines.append("| Rank | Repository | Tags | Stars | Weekly Δ | Forks | Updated | Relevance | Score |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for idx, row in enumerate(rows, start=1):
        lines.append(
            f"| {idx} | [{row.full_name}]({row.html_url}) | {row.tags} | {row.stars} | "
            f"{row.weekly_star_delta:.1f} | {row.forks} | {row.updated_days:.1f}d | {row.relevance:.1f} | {row.score:.1f} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, help="Path to JSON export")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--theme", choices=["general", "marketing"], default="general")
    args = parser.parse_args()

    if args.input:
        payload = json.loads(args.input.read_text())
    else:
        payload = json.load(sys.stdin)

    if not isinstance(payload, list):
        raise SystemExit("expected a JSON array of repository objects")

    now = datetime.now(timezone.utc)
    rows = [row for row in (score_repo(item, now, theme=args.theme) for item in payload) if row is not None]
    rows.sort(key=lambda r: (r.score, r.weekly_star_delta, r.stars, r.forks), reverse=True)
    rows = rows[: args.limit]

    print(render(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

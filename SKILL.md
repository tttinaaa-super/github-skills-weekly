---
name: github-skills-weekly
description: Find active GitHub repositories that contain a SKILL.md file, then rank them weekly by new stars, recency, forks, and activity so you can publish a fresh leaderboard.
---

# GitHub Skills Weekly

## What This Skill Does

Use this skill to build a weekly leaderboard of active GitHub repositories that contain a `SKILL.md` file.
It is meant for discovery work: scanning the GitHub ecosystem, filtering to maintained repos, and ranking candidates for a newsletter, digest, or internal watchlist.

## When To Use It

- You want a weekly roundup of notable skill repos.
- You need to find fresh or recently updated repositories that ship `SKILL.md`.
- You want a ranked view based on stars, recent star growth, forks, and update recency.
- You want a repeatable query/reporting workflow rather than a one-off search.
- You want the shortlist filtered toward non-coding skills that help with marketing, writing, presentations, docs, spreadsheets, Slack, or daily computer work.

## Workflow

1. Collect candidate repositories.
2. Verify each repo actually contains `SKILL.md`.
3. Measure activity signals.
4. Normalize and rank the results.
5. Write out a weekly report with the cutoff date and score breakdown.

## Collection Rules

- Search GitHub for repositories that mention `SKILL.md` or are clearly skill-related.
- Prefer repos with recent commits or releases.
- Exclude archived or empty repos when possible.
- When results are noisy, tighten the search by language, topic, or recent activity window.

## Ranking Signals

Use a weighted score built from:

- New stars during the week.
- Repository update recency.
- Fork count.
- Recent commit or release activity.
- Optional bonus for repos that add or update `SKILL.md` recently.
- Relevance to marketing or productivity workflows.

If exact week-over-week star deltas are unavailable, use the best available proxy and note it in the report.

## Filtering Preference

Prefer skills that help with:

- Brand and visual consistency.
- Decks, docs, and reporting.
- Internal communication and coordination.
- File handling, summarization, and light automation.
- Personal productivity on a computer.

Deprioritize skills that are primarily:

- Software engineering or infrastructure.
- Deep coding, debugging, or framework-specific developer tooling.
- Purely technical demos with little day-to-day usefulness for a marketer.

If the candidate pool is small, keep the report honest and say so instead of padding the list.

## Output Format

Produce a table with:

- Rank
- Repository
- Owner
- Stars
- Star change
- Forks
- Last updated
- Why it ranked here

Add a short methodology note that explains the search window and any proxy metrics used.

## Script

Use `scripts/weekly_rank.py` when you want a repeatable local summary from exported repository data.
The script expects JSON input from a GitHub query or API export and outputs a ranked Markdown table.
It supports a `--theme marketing` mode that boosts presentation, writing, communication, docs, and productivity-oriented results.

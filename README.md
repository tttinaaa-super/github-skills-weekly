# GitHub Skills Weekly

Weekly GitHub discovery for marketing-friendly, productivity-focused, and general skill-growth resources.

## What this repo does

- Finds active GitHub repositories, tools, and skill resources
- Ranks them by recent stars, recency, forks, and activity
- Biases results toward things that are useful for marketing, writing, decks, docs, spreadsheets, Slack, daily computer work, and general skill growth

## Files

- `SKILL.md` - Codex skill instructions
- `agents/openai.yaml` - UI metadata for the skill picker
- `scripts/weekly_rank.py` - Rank exported repository data into a Markdown leaderboard
- `scripts/generate_weekly_report.py` - Fetch GitHub weekly candidates and generate a report

## How to use the ranking script

```bash
python3 scripts/weekly_rank.py --input repos.json --theme marketing --limit 10
```

`repos.json` should be a JSON array of repository objects. Each object can include:

- `full_name`
- `html_url`
- `stargazers_count`
- `fork_count` or `forks_count`
- `updated_at`
- `pushed_at`
- `weekly_star_delta`
- `has_skill_md`
- `archived`

## Weekly automation

This repo includes a GitHub Actions workflow that runs weekly, regenerates a Markdown report, and commits it back into the repository.

You need to add a repository secret named `GH_TOKEN` with permission to read repository data and push commits back to this repo.

## Output

The automation writes a report to:

- `reports/weekly-skills.md`

The report is sorted for marketing, productivity, and skill-growth relevance first, not just raw developer-tool popularity.
Each row is tagged with `marketing`, `productivity`, `skill-growth`, or `general` so you can scan the list quickly.

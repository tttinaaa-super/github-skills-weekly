# GitHub Skills Weekly

Weekly GitHub skill discovery for non-coding, marketing-friendly, and productivity-focused workflows.

## What this repo does

- Finds active GitHub repositories that contain `SKILL.md`
- Ranks them by recent stars, recency, forks, and activity
- Biases results toward skills that are useful for marketing, writing, decks, docs, spreadsheets, Slack, and daily computer work

## Files

- `SKILL.md` - Codex skill instructions
- `agents/openai.yaml` - UI metadata for the skill picker
- `scripts/weekly_rank.py` - Rank exported repository data into a Markdown leaderboard

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

The report is sorted for marketing and daily productivity relevance first, not just raw developer-tool popularity.

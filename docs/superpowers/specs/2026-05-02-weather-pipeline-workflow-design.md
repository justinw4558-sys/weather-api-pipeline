# Weather Pipeline GitHub Actions Workflow — Design Spec

**Date:** 2026-05-02
**Repo:** weather-api-pipeline

---

## Goal

Automate `weather.py` to run on a weekly schedule via GitHub Actions, committing the updated `weather_data.csv` back to the repo after each run. Failures must be visible (red run, not silently swallowed).

---

## Triggers

- `workflow_dispatch` — manual trigger for testing before trusting the schedule
- `schedule` — cron `0 0 * * 0` (every Sunday at midnight UTC)

---

## Workflow Structure

Single job on `ubuntu-latest`.

**Steps:**
1. Checkout repo (`actions/checkout`)
2. Set up Python 3.12 (`actions/setup-python`)
3. Install dependencies (`pip install -r requirements.txt`)
4. Run `weather.py` — non-zero exit fails the job visibly
5. Commit `weather_data.csv` back with message `chore: update weather data [skip ci]` and push

**Permissions:** `contents: write` (required for the commit-back step)

**`[skip ci]` tag:** Prevents the commit-back from triggering another workflow run loop.

---

## Secrets

One secret required: `WEATHER_API_KEY`

- Add via: repo → Settings → Secrets and variables → Actions → New repository secret
- `weather.py` already reads it via `os.getenv("WEATHER_API_KEY")` — no code changes needed

---

## Error Handling

If `weather.py` exits with a non-zero status code (API failure, bad key, rate limit, network error), the job fails and GitHub marks the run red. No silent failures.

---

## File Written

`.github/workflows/weather-pipeline.yml`

---

## Success Criteria

- Manual trigger runs green and a new commit with updated `weather_data.csv` appears on `main`
- GitHub Actions tab shows the schedule attached to the workflow
- `.env` does not appear anywhere in the workflow file or repo

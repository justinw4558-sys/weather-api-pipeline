# Weather Pipeline GitHub Actions Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a GitHub Actions workflow that runs `weather.py` on a weekly schedule and commits the updated `weather_data.csv` back to the repo.

**Architecture:** Single workflow file with one job. Job checks out the repo, installs Python deps, runs the script, then commits and pushes `weather_data.csv` back to `main`. Manual trigger included for testing before the schedule fires.

**Tech Stack:** GitHub Actions, Python 3.12, `actions/checkout`, `actions/setup-python`

---

### Task 1: Create the workflow directory and file

**Files:**
- Create: `.github/workflows/weather-pipeline.yml`

- [ ] **Step 1: Create the workflows directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Create `.github/workflows/weather-pipeline.yml` with this exact content**

```yaml
name: Weather Pipeline

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * 0"  # Every Sunday at midnight UTC

permissions:
  contents: write

jobs:
  run-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run weather pipeline
        env:
          WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
        run: python weather.py

      - name: Commit updated weather data
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add weather_data.csv
          git diff --cached --quiet || git commit -m "chore: update weather data [skip ci]"
          git push
```

- [ ] **Step 3: Verify the file was created**

```bash
cat .github/workflows/weather-pipeline.yml
```

Expected: full YAML printed to terminal with no errors.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/weather-pipeline.yml
git commit -m "feat: add GitHub Actions workflow for weather pipeline"
```

---

### Task 2: Push to GitHub and add the secret

**Files:**
- No file changes — GitHub UI configuration step

- [ ] **Step 1: Push the workflow to GitHub**

```bash
git push
```

Expected: branch pushed, no errors.

- [ ] **Step 2: Add the `WEATHER_API_KEY` secret to the repo**

In your browser:
1. Go to your `weather-api-pipeline` repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `WEATHER_API_KEY`
5. Value: your WeatherAPI key (the same value from your local `.env` file)
6. Click **Add secret**

---

### Task 3: Run manually and verify

**Files:**
- No file changes — verification step

- [ ] **Step 1: Trigger the workflow manually**

In your browser:
1. Go to your `weather-api-pipeline` repo on GitHub
2. Click the **Actions** tab
3. Click **Weather Pipeline** in the left sidebar
4. Click **Run workflow** → **Run workflow**

- [ ] **Step 2: Watch the run complete**

Wait for the run to finish (roughly 1-2 minutes). The run should show a green checkmark.

Click into the run and expand each step to confirm:
- "Run weather pipeline" step shows city forecasts printed to the log
- "Commit updated weather data" step shows a commit was made (or "nothing to commit" if the data hasn't changed)

- [ ] **Step 3: Verify the commit appeared on main**

Go to your repo's main page on GitHub. The most recent commit should be:
`chore: update weather data [skip ci]`

(or confirm via terminal: `git pull && git log --oneline -3`)

- [ ] **Step 4: Verify the schedule is shown**

On the **Actions** tab → **Weather Pipeline** workflow page, GitHub should display:
> "This workflow has a schedule."

---

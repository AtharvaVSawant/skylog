# SkyLog — Live Weather Intelligence Dashboard

An end-to-end data pipeline: a Python script pulls current weather for 10
cities from the OpenWeatherMap API, logs each reading to a SQLite
database, and Power BI visualizes the growing historical dataset —
current conditions, temperature trends, hot/cold comparisons, weather
condition breakdown, and a color-coded map. A GitHub Actions workflow
runs the pull automatically every hour, so the dataset keeps growing
without anyone needing to run anything manually.

## Key Metrics

| Metric               | Value                                                             |
|-----------------------|--------------------------------------------------------------------|
| Cities tracked         | 10 (Mumbai, Delhi, Bangalore, Chennai, Kolkata, Pune, New York, London, Tokyo, Sydney) |
| Refresh interval        | Hourly, via GitHub Actions                                        |
| Data source              | OpenWeatherMap Current Weather API                                |
| Database                  | SQLite (`weather_data.db`), committed back to the repo each run  |
| Fields per reading        | temperature, feels-like, humidity, wind speed, condition, description, lat/lon, timestamp |

## Architecture

```
OpenWeatherMap API
       │
       ▼
weather_pull.py   (Python: requests + sqlite3)
       │
       ▼
weather_data.db   (SQLite — weather_log table, append-only)
       │
       │  ▲
       │  │  GitHub Actions runs this hourly (.github/workflows/weather-pull.yml)
       │  │  and commits the updated .db back to the repo
       │  └────────────────────────────────
       ▼
git pull           (locally, to sync the latest .db)
       │
       ▼
Power BI Desktop   (SQLite connector → Refresh)
       │
       ▼
Dashboard: KPI cards, temperature trend, hot/cold bar chart,
           weather condition donut, city map
```

## How the automation works

Instead of relying on a machine staying on with a local scheduled task,
data collection runs entirely in GitHub Actions:

1. `.github/workflows/weather-pull.yml` triggers every hour (`cron: '0 * * * *'`),
   plus supports a manual "Run workflow" button for on-demand testing.
2. It installs dependencies, runs `weather_pull.py` using an API key stored
   as a GitHub Actions secret (`OPENWEATHER_API_KEY`) — never committed in
   plain text — and commits the updated `weather_data.db` back to `main`.
3. Locally, running `git pull` fetches that updated database file.
4. Opening the `.pbix` in Power BI Desktop and clicking **Refresh** loads
   the new rows into the dashboard.

## Setup

1. Clone this repo.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your own OpenWeatherMap API key
   (for running the script locally/testing).
4. For the GitHub Actions workflow to run in your own fork, add your key
   as a repository secret: **Settings → Secrets and variables → Actions →
   New repository secret** → name it `OPENWEATHER_API_KEY`.
5. Run once locally to test:
   ```bash
   python weather_pull.py
   ```
6. Open Power BI Desktop → Get Data → SQLite → select `weather_data.db`.
7. To pick up new data later: `git pull`, then click **Refresh** in
   Power BI Desktop.

## Screenshot

*(add a screenshot of the finished dashboard here)*

## What I'd Improve Next

- Move from SQLite to a hosted database (e.g. Postgres) so Power BI
  Service could refresh on a schedule directly, without needing a local
  file or gateway.
- Add a forecast table (5-day forecast endpoint) alongside current
  conditions, for a "predicted vs. actual" visual.
- Publish to Power BI Service with a real scheduled refresh once the data
  source is cloud-hosted.
- Add basic alerting (e.g. flag extreme temperature swings) using a
  simple threshold check in the Python script.

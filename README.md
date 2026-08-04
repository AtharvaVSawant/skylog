# SkyLog — a weather dashboard

An end-to-end data pipeline: a Python script pulls current weather for 10
global cities from the OpenWeatherMap API, logs each reading to a SQLite
database, and Power BI visualizes the growing historical dataset —
current conditions, temperature trends, and a color-coded map.

## Key Metrics

| Metric                  | Value                                      |
|--------------------------|---------------------------------------------|
| Cities tracked            | 10 (5 Indian metros + 5 global)            |
| Refresh interval          | Hourly (cron / Task Scheduler)             |
| Data source                | OpenWeatherMap Current Weather API        |
| Database                    | SQLite                                     |
| Fields per reading         | temp, feels-like, humidity, wind, condition, lat/lon, timestamp |

## Architecture

```
OpenWeatherMap API
       │
       ▼
weather_pull.py  (Python: requests + sqlite3)
       │
       ▼
weather_data.db  (SQLite — weather_log table, append-only)
       │
       ▼
Power BI Desktop  (SQLite connector)
       │
       ▼
Dashboard: current-condition cards, trend lines, hot/cold bar chart, map
```

## Setup

1. Clone this repo.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your own OpenWeatherMap API key.
4. Run once to test:
   ```bash
   python weather_pull.py
   ```
5. Schedule it hourly via cron (Mac/Linux) or Task Scheduler (Windows) —
   see comments in `weather_pull.py` / `weather_scheduler.py`.
6. Open Power BI Desktop → Get Data → SQLite → select `weather_data.db`.

## Screenshot

*(add a screenshot of the finished dashboard here)*

## What I'd Improve Next

- Move from SQLite to PostgreSQL for concurrent read/write safety once the
  log gets large.
- Add a forecast table (5-day forecast endpoint) alongside current
  conditions, for a "predicted vs. actual" visual.
- Publish to Power BI Service with a real scheduled refresh (via gateway)
  instead of manual refresh in Desktop.
- Add basic alerting (e.g. flag extreme temperature swings) using a
  simple threshold check in the Python script.
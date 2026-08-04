"""
weather_scheduler.py
Runs weather_pull.py on a loop, once per hour, for demo purposes.
Ctrl+C to stop. For production use, prefer cron / Task Scheduler instead
(see README) so it doesn't depend on a terminal staying open.
"""

import time
from datetime import datetime

from weather_pull import run_once

INTERVAL_SECONDS = 60 * 60  # 1 hour

if __name__ == "__main__":
    print("Starting weather scheduler. Press Ctrl+C to stop.")
    while True:
        print(f"\n--- Run at {datetime.now().isoformat(timespec='seconds')} ---")
        run_once()
        print(f"Sleeping for {INTERVAL_SECONDS // 60} minutes...")
        time.sleep(INTERVAL_SECONDS)

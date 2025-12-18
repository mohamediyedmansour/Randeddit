#!/usr/bin/env python3
import csv
import time
import random
import threading
from pathlib import Path
from queue import Queue, Empty

from playwright.sync_api import sync_playwright, TimeoutError
from tqdm import tqdm

# ================= CONFIG =================

START_PAGE = 1
END_PAGE = 1433

WORKERS = 3                 # DO NOT increase
MAX_RETRIES = 3
PAGE_TIMEOUT = 45000        # ms
DELAY_RANGE = (1.5, 3.5)    # seconds

BASE_URL = "https://www.reddit.com/best/communities/{}"

OUTPUT_CSV = Path("../assets/subreddits.csv")
FAILED_PAGES = Path("./failed_pages.txt")

# =========================================

lock = threading.Lock()
seen = set()


def ensure_csv():
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    if not OUTPUT_CSV.exists() or OUTPUT_CSV.stat().st_size == 0:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["subreddit", "members", "description"]
            )
            writer.writeheader()


def load_existing():
    if not OUTPUT_CSV.exists():
        return
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("subreddit"):
                seen.add(row["subreddit"])


def write_row(row):
    with lock:
        with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["subreddit", "members", "description"]
            )
            writer.writerow(row)


def log_failed(page_number):
    with lock:
        with open(FAILED_PAGES, "a") as f:
            f.write(f"{page_number}\n")


def human_delay():
    time.sleep(random.uniform(*DELAY_RANGE))


def worker(queue: Queue, progress):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # IMPORTANT
            args=["--disable-blink-features=AutomationControlled"],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )

        page = context.new_page()

        while True:
            try:
                page_number = queue.get_nowait()
            except Empty:
                break

            url = BASE_URL.format(page_number)

            success = False

            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    page.goto(
                        url,
                        timeout=PAGE_TIMEOUT,
                        wait_until="domcontentloaded",
                    )

                    page.wait_for_selector(
                        "div[data-community-id]",
                        timeout=PAGE_TIMEOUT,
                    )

                    divs = page.query_selector_all("div[data-community-id]")
                    added = 0
                    sample = None

                    for div in divs:
                        name = div.get_attribute("data-prefixed-name")
                        if not name or name in seen:
                            continue

                        row = {
                            "subreddit": name.strip(),
                            "members": (div.get_attribute("data-subscribers-count") or "").strip(),
                            "description": " ".join(
                                (div.get_attribute("data-public-description-text") or "").split()
                            ),
                        }

                        seen.add(name)
                        write_row(row)
                        added += 1
                        sample = sample or name

                    print(
                        f"✔ Page {page_number} scraped ({added} new)"
                        + (f" | Sample: {sample}" if sample else "")
                    )

                    success = True
                    break

                except TimeoutError:
                    print(f"⏱ Page {page_number} timeout (attempt {attempt})")
                    human_delay()

                except Exception as e:
                    print(f"✖ Page {page_number} error: {e}")
                    break

            if not success:
                print(f"✖ Page {page_number} failed after {MAX_RETRIES} retries")
                log_failed(page_number)

            human_delay()
            progress.update(1)
            queue.task_done()

        browser.close()


def main():
    ensure_csv()
    load_existing()

    queue = Queue()
    for i in range(START_PAGE, END_PAGE + 1):
        queue.put(i)

    progress = tqdm(total=queue.qsize(), desc="Scraping pages")

    threads = []
    for _ in range(WORKERS):
        t = threading.Thread(target=worker, args=(queue, progress), daemon=True)
        t.start()
        threads.append(t)

    try:
        queue.join()
    except KeyboardInterrupt:
        print("\n⛔ Interrupted — data safely saved")

    progress.close()
    print(f"\n✅ Finished. Unique subreddits: {len(seen)}")
    print(f"⚠ Failed pages saved to: {FAILED_PAGES}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import csv
from pathlib import Path

INPUT_CSV = Path("../assets/subreddits.csv")
OUTPUT_TXT = Path("../assets/subreddits.txt")


def main():
    seen = set()
    names = []

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        for row in reader:
            if not row:
                continue

            raw = row[0].strip()  # subreddit column
            if not raw:
                continue

            # remove "r/" prefix if present
            name = raw[2:] if raw.lower().startswith("r/") else raw

            if name not in seen:
                seen.add(name)
                names.append(name)

    OUTPUT_TXT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

    print(f"✅ Wrote {len(names)} subreddits to {OUTPUT_TXT}")


if __name__ == "__main__":
    main()

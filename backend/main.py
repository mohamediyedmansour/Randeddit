from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import os
import csv

app = FastAPI(
    title="Random Subreddit API",
    description="Fetch random subreddits or search subreddits efficiently.",
    version="1.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBREDDIT_FILE = "./assets/subreddits.txt"
CSV_FILE = "./assets/subreddits.csv"

line_offsets = []
csv_index = {}  

# Random subreddit indexing
def build_index(file_path: str):
    offsets = []
    offset = 0
    with open(file_path, "rb") as f:
        for line in f:
            offsets.append(offset)
            offset += len(line)
    return offsets

if os.path.exists(SUBREDDIT_FILE):
    print("Building random access index for subreddits.txt...")
    line_offsets = build_index(SUBREDDIT_FILE)
    TOTAL_LINES = len(line_offsets)
    print(f"Index built: {TOTAL_LINES} lines found")
else:
    raise FileNotFoundError(f"{SUBREDDIT_FILE} not found!")

def get_random_line(file_path: str) -> str:
    random_index = random.randint(0, TOTAL_LINES - 1)
    offset = line_offsets[random_index]
    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(offset)
        line = f.readline().strip()
        # Strip r/ if present
        if line.lower().startswith("r/"):
            line = line[2:]
        return line, random_index

# CSV indexing for fast search
def build_csv_index(file_path: str):
    """
    Builds memory-efficient index: subreddit_name.lower() -> file byte offset
    """
    index = {}
    with open(file_path, "rb") as f:
        header = f.readline()  # skip header
        offset = f.tell()
        while True:
            line = f.readline()
            if not line:
                break
            decoded_line = line.decode("utf-8").strip()
            if not decoded_line:
                offset = f.tell()
                continue
            subreddit_name = decoded_line.split(",", 1)[0].strip().lower()
            if subreddit_name.startswith("r/"):
                subreddit_name = subreddit_name[2:]
            index[subreddit_name] = offset
            offset = f.tell()
    return index

if os.path.exists(CSV_FILE):
    print("Building CSV index for fast subreddit search...")
    csv_index = build_csv_index(CSV_FILE)
    print(f"CSV index built: {len(csv_index)} subreddits found")
else:
    raise FileNotFoundError(f"{CSV_FILE} not found!")

def get_subreddit_info(subreddit_name: str, include_r_prefix: bool = True):
    """
    Retrieve subreddit info from CSV by using the index.
    include_r_prefix: True for search (keep r/), False for random (strip r/)
    """
    key = subreddit_name.lower().lstrip("r/")
    if key not in csv_index:
        return None
    offset = csv_index[key]
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        f.seek(offset)
        line = f.readline().strip()
        if not line:
            return None
        reader = csv.DictReader([line], fieldnames=["subreddit", "members", "description"])
        row = next(reader)
        sub_name = row['subreddit']
        if not include_r_prefix:
            sub_name = sub_name.lstrip("r/")
        return {
            "subreddit": sub_name,
            "members": int(row['members']),
            "description": row['description']
        }

# FastAPI Endpoints
@app.get("/get_sub", summary="Get one or multiple random subreddits with full info")
async def get_random_subreddit(count: int = Query(1, ge=1, le=10, description="Number of subreddits to return (1-10)")):
    try:
        results = []
        for _ in range(count):
            subreddit_name, line_number = get_random_line(SUBREDDIT_FILE)
            info = get_subreddit_info(subreddit_name, include_r_prefix=False)
            if info:
                info["line_number"] = line_number
                results.append(info)
            else:
                results.append({"subreddit": subreddit_name, "line_number": line_number})
        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/search_sub", summary="Search for a subreddit by name")
async def search_sub(subreddit: str = Query(..., description="Subreddit name to search for, e.g., feedthebeast")):
    try:
        result = get_subreddit_info(subreddit)
        if result:
            return result
        return JSONResponse(status_code=404, content={"error": "Subreddit not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
@app.head("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

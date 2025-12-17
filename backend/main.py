from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import os

app = FastAPI(
    title="Random Subreddit API",
    description="A simple API to fetch a random subreddit from a huge list of subreddits.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBREDDIT_FILE = "./assets/subreddits.txt"
line_offsets = []

# Precompute line offsets for fast random access
def build_index(file_path: str):
    offsets = []
    offset = 0
    with open(file_path, "rb") as f:
        for line in f:
            offsets.append(offset)
            offset += len(line)
    return offsets

if os.path.exists(SUBREDDIT_FILE):
    print("Building index for fast random access... (only once)")
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
        return f.readline().strip(), random_index

@app.get("/get_sub", summary="Get a random subreddit", response_description="A random subreddit")
async def get_random_subreddit():
    try:
        subreddit, line_number = get_random_line(SUBREDDIT_FILE)
        return {"subreddit": subreddit, "line_number": line_number}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

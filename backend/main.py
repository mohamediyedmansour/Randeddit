from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random

app = FastAPI(
    title="Random Subreddit API",
    description="""
    A simple API to fetch a random subreddit from a huge list of subreddits.

    - `/get_sub`: Returns a random subreddit`.
    """,
    version="1.0.0"
)

# CORS to connect from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUBREDDIT_FILE = "./assets/subreddits.txt"
TOTAL_LINES = 4074185

def get_random_line(file_path: str, line_number: int) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        for current_number, line in enumerate(f):
            if current_number == line_number:
                return line.strip()
    return None

@app.get("/get_sub", summary="Get a random subreddit", response_description="A random subreddit")
async def get_random_subreddit():
    #return random line 
    random_index = random.randint(0, TOTAL_LINES)
    subreddit = get_random_line(SUBREDDIT_FILE, random_index)

    if subreddit is None:
        return JSONResponse(status_code=500, content={"error": "Could not read subreddit line."})

    return {"subreddit": subreddit, "line_number": random_index}


# uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

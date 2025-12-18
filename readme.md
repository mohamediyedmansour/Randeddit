# Randomdit

**Randomdit** is a Chrome extension + backend service that lets you instantly discover random subreddits.
It adds a **Random** button directly into Reddit’s UI and also provides a popup experience powered by a custom backend API.

> 🎥 **Demo video**: _Coming soon_ (placeholder — will be added here)

---

## ✨ Features

- 🎲 One‑click random subreddit discovery
- 🧠 Prefetching for instant navigation
- 🧩 Seamless Reddit UI integration
- 🚀 Fast backend powered by Docker
- 📊 Large dataset of scraped subreddits

---

## 🧩 Browser Support

- ✅ **Chrome**: Fully supported
- 🚧 **Firefox**: Not supported yet (work in progress)

---

## 📦 Chrome Extension Installation (Manual)

Chrome Web Store publishing is not enabled yet. To install manually:

1. **Download the extension**  
   https://github.com/mohamediyedmansour/Randeddit/releases/download/v1.0.0/randomdit.zip

2. **Unzip** the file into any folder on your system

3. Open Chrome and go to:

   ```
   chrome://extensions
   ```

4. Enable **Developer mode** (top‑right corner)

5. Click **Load unpacked**

6. Select the **unzipped folder**

✅ The Randomdit button will now appear on Reddit.

---

## 🐳 Backend Setup (API Server)

The backend powers random subreddit fetching.

### 1️⃣ Install Docker Compose

```bash
sudo apt update && sudo apt install docker-compose
```

### 2️⃣ Start the Backend

```bash
cd backend
docker-compose up --build
```

The API will be available once the containers are running.

---

## 🧪 Tools Folder (Scraping & Dataset Generation)

The `tools/` folder is used to scrape subreddit data from Reddit and prepare datasets.

### 1️⃣ Create a Virtual Environment

```bash
cd tools
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 2️⃣ Install Playwright Chromium

```bash
playwright install chromium
```

> ⚠️ Required only if you want to scrape data yourself

### 3️⃣ Run the Scrapers

```bash
./scrape_subs.py
./clean_file.py
```

This will:

- Scrape subreddit names
- Capture member counts & descriptions
- Output:
  - `subreddits.csv`
  - `subreddits.txt`

---

## ⬇️ Skip Scraping (Download Dataset)

If you **don’t want to run Playwright**, you can directly download the dataset:

```bash
wget https://github.com/mohamediyedmansour/Randeddit/raw/refs/heads/main/backend/assets/subreddits.csv
```

Includes:

- Subreddit name
- Member count
- Description

---

## 🚧 Project Status

- Chrome extension: ✅ Stable
- Backend API: ✅ Stable
- Firefox support: 🚧 In progress
- Demo video: ⏳ Coming soon

---

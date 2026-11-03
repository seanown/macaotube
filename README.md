# MacaoTube

Macau tourism and culture on YouTube, refreshed daily: official videos from the
Macao Government Tourism Office (澳門旅遊局) and the Cultural Affairs Bureau
(文化局), plus the independent English-language creators people actually watch.

## How it works

| Step | Script | Quota cost |
|---|---|---|
| Pull every upload from the official channels | `official.py` | ~150 units |
| Search 25 Macau queries for independent creators | `fetch.py` | ~4,200 units |
| Filter, classify by topic, score | `rerank.py` | none |
| Write the web page | `build.py` → `site/index.html` | none |

The free YouTube Data API quota is 10,000 units a day, so one daily run fits comfortably.

**Score** = breakout (views ÷ channel average, capped at 50×) + engagement
(likes + 2 × comments per view) + freshness (halves every 18 months) + a small
boost for festival, heritage, arts, tradition and food videos.

## Setup

1. Add a repository secret named `YT_KEY` with your YouTube Data API key
   (Settings → Secrets and variables → Actions).
2. Set Settings → Pages → Source to **GitHub Actions**.
3. Run the workflow once from the Actions tab (Refresh and publish → Run workflow).

The site then rebuilds every day at 02:13 Macau time.

## Run locally

```
YT_KEY=your-key python official.py
YT_KEY=your-key python fetch.py
python rerank.py && python build.py   # open site/index.html
```

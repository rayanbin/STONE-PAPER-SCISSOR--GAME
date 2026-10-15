# Stone Paper Scissors — AI Battle

A browser-based Stone, Paper, Scissors game powered by **Python Flask**. Play against an adaptive computer opponent, watch the hand animations, and track your wins, losses, ties, and win percentage.

## Run locally

1. Install Python 3.10 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Deploy on Vercel

Import this repository into Vercel and leave **Root Directory** set to the repository root. Vercel will detect the root `app.py` Flask application and install `requirements.txt`.

For production, add a strong `SECRET_KEY` environment variable in Vercel Project Settings → Environment Variables, then redeploy.

## Features

- Python Flask backend
- Adaptive computer opponent
- Animated Stone, Paper, Scissors choices
- Per-browser session scoreboard
- Responsive browser-based interface

**Note:** Scoreboard data is stored in the player's signed session cookie, so it is per browser and is not a shared global leaderboard.

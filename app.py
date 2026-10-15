import os
import random
from flask import Flask, render_template, jsonify, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "heightmesh-game-dev-key-change-in-vercel")

CHOICES = {0: "Stone 🪨", 1: "Paper 📄", 2: "Scissors ✂️"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play/<int:userdata>")
def play(userdata):
    if userdata not in CHOICES:
        return jsonify({"error": "Invalid move"}), 400

    # Keep each player's history and scoreboard in their signed session cookie.
    history = session.get("history", [])
    wins = int(session.get("wins", 0))
    losses = int(session.get("losses", 0))
    ties = int(session.get("ties", 0))

    # Basic adaptive opponent: predict the player's most common next move.
    if len(history) < 2:
        comp = random.randint(0, 2)
    else:
        last_move = history[-1]
        following_moves = [
            history[i + 1] for i in range(len(history) - 1)
            if history[i] == last_move
        ]
        if following_moves:
            predicted_user = max(set(following_moves), key=following_moves.count)
        else:
            predicted_user = max(set(history), key=history.count)
        comp = (predicted_user + 1) % 3
        if random.random() < 0.25:
            comp = random.randint(0, 2)

    if userdata == comp:
        result = "It's a Tie! 🤝"
        ties += 1
    elif (userdata == 0 and comp == 2) or (userdata == 1 and comp == 0) or (userdata == 2 and comp == 1):
        result = "You Win! 🎉"
        wins += 1
    else:
        result = "AI Wins! 🤖"
        losses += 1

    history.append(userdata)
    # Avoid unbounded cookie growth.
    session["history"] = history[-50:]
    session["wins"] = wins
    session["losses"] = losses
    session["ties"] = ties

    total_games = wins + losses + ties
    win_percentage = round((wins / total_games) * 100, 1) if total_games else 0.0

    response = jsonify({
        "user": CHOICES[userdata],
        "comp": CHOICES[comp],
        "result": result,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "total": total_games,
        "win_percentage": win_percentage,
    })
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

history = []
choices = {0: "Stone 🪨", 1: "Paper 📄", 2: "Scissors ✂️"}

# Scoreboard variables
wins = 0
losses = 0
ties = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play/<int:userdata>')
def play(userdata):
    global history, wins, losses, ties
    
    # AI Brain Logic
    if len(history) < 2:
        comp = random.randint(0, 2)
    else:
        last_move = history[-1]
        following_moves = [history[i+1] for i in range(len(history)-1) if history[i] == last_move]
        if following_moves:
            predicted_user = max(set(following_moves), key=following_moves.count)
        else:
            predicted_user = max(set(history), key=history.count)
        comp = (predicted_user + 1) % 3
        if random.random() < 0.25:
            comp = random.randint(0, 2)

    history.append(userdata)

    # Result Logic & Scoreboard Update
    if userdata == comp:
        result = "It's a Tie! 🤝"
        ties += 1
    elif (userdata == 0 and comp == 2) or (userdata == 1 and comp == 0) or (userdata == 2 and comp == 1):
        result = "You Win! 🎉"
        wins += 1
    else:
        result = "AI Wins! 🤖"
        losses += 1

    total_games = wins + losses + ties
    win_percentage = round((wins / total_games) * 100, 1) if total_games > 0 else 0.0

    return jsonify({
        "user": choices[userdata],
        "comp": choices[comp],
        "result": result,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "total": total_games,
        "win_percentage": win_percentage
    })

if __name__ == '__main__':
    app.run(debug=True)
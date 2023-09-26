from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"

boggle_game = Boggle()


@app.route("/")
def home():
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("board.html", board=board, highscore=session.get("highscore", 0), plays=session.get("plays", 0))


@app.route("/check-guess", methods=["POST"])
def check_guess():
    guess = request.json["guess"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)
    return jsonify(result=response)


@app.route("/end-game", methods=["POST"])
def end_game():
    score = request.json["score"]
    session["plays"] = session.get("plays", 0) + 1
    highscore = session.get("highscore", 0)
    new_record = False

    if score > highscore:
        session["highscore"] = score
        new_record = True

    # For debugging purposes
    print(f"High score: {session['highscore']}")
    print(f"Number of plays: {session['plays']}")

    return jsonify(newRecord=new_record)


if __name__ == "__main__":
    app.run(debug=True)

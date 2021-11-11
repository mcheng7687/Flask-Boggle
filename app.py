from flask.json import jsonify
from boggle import Boggle
from flask import Flask, render_template, redirect, session, request, flash, jsonify

boggle_game = Boggle()
board = boggle_game.make_board()

app = Flask(__name__)
app.config["SECRET_KEY"] = "password"


@app.route("/")
def home():
    """Home page with START button"""
    global board
    board = boggle_game.make_board()
    
    return render_template("home.html")

@app.route("/game")
def game():
    """Game page where board, timer, high score, and current score are displayed"""

    highScore = session.get("high_score",0)
    visits = session.get("visits",0)
    return render_template("game.html", board = board, cols = len(board), rows = len(board[0]), highScore = highScore)

@app.route("/new-game")
def newGame():
    """New game to reset current score and board"""
    return redirect("/")

@app.route("/test-word/<word>",methods=["POST"])
def testWord(word):
    """Given a word, this returns TRUE if word is verified and FALSE otherwise. 
    Returns POINT VALUE based on word length """
    return jsonify({"word": word})
    #return {"result": boggle_game.check_valid_word(board,word), "points": len(word)}
    

@app.route("/game-over",methods=["GET"])
def endGame():
    """End the game and retrieves score. If score is higher than high score, 
    than return TRUE otherwise return FALSE."""
    score = int(request.args.get("score"))
    high=checkHighScore(score)
    
    return render_template("end.html", high=high)

@app.route("/reset")
def reset():
    """Reset high score and number of visits to zero."""
    session['high_score'] = 0
    session['visits'] = 0
    return redirect("/")


def checkHighScore(score):
    """Checks if score is higher than high score. 
    Return TRUE if score is higher and set new high score as score. 
    Return FALSE if score is lower or equal to high score."""
    if (score > session['high_score']):
        session['high_score'] = score
        return True
    return False
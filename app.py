from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DEBUG"] = True
Session(app)

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



@app.route("/")
def index():

    
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
    


    return render_template("game.html", board=session["board"], turn=session["turn"])

@app.route("/reset")
def reset():

    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"

    return redirect("/")


@app.route("/play/<int:row>/<int:col>")
def play(row,col):

    session["board"][row][col] = session["turn"]

    session["winX"] = ["X","X","X"]
    session["winO"] = ["O","O","O"]

    

    #check for horizontal wins
    for item in session["board"]:
        if item == session["winX"]:
            return render_template("winner.html", winner = "X")
        if item == session["winO"]:
            return render_template("winner.html", winner = "O")
    
    
    #check for vertical wins
    session["vertical"] = []
    session["vertical2"] = []
    session["vertical3"] = []

    for i in session["board"]:
        session["vertical"].append(i[0])
        session["vertical2"].append(i[1])
        session["vertical3"].append(i[2])
    
    session["verticalcheck"] = [session["vertical"], session["vertical2"], session["vertical3"]]
    
    for item in session["verticalcheck"]:
        if item == session["winX"]:
            return render_template("winner.html", winner = "X")
        if item == session["winO"]:
            return render_template("winner.html", winner = "O")
    
    #check for diagonal wins
    session["diagonalcheck1"] = []
    session["diagonalcheck2"] = []
    count = 0
    count2 = 2

    for i in session["board"]:
        session["diagonalcheck1"].append(i[count])
        session["diagonalcheck2"].append(i[count2])
        count = count + 1
        count2 = count2 - 1
    
    session["diagonalcheck"] = [session["diagonalcheck1"], session["diagonalcheck2"]]

    for item in session["diagonalcheck"]:
        if item == session["winX"]:
            return render_template("winner.html", winner = "X")
        if item == session["winO"]:
            return render_template("winner.html", winner = "O")

    #check for stalemate
    empty = 0

    for i in session["board"]:
        for j in i:
            if j == None:
                empty = empty + 1
    
    if empty == 0:
        return render_template("winner.html", winner = "NOBODY")
           


    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"

    
    return redirect("/")
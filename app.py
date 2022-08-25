from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789"

@app.route('/')
def main_page():
    """ Create board """
    session['board'] = boggle_game.make_board()
    return render_template('index.html')

@app.route("/check", methods=["POST"])
def check():
    """ Check if word's validity """
    return jsonify({'response': boggle_game.check_valid_word(session["board"], request.json["guess"].lower())})

@app.route("/update", methods=["POST"])
def update():
    """ Update nplay and highest score and return a JSON response with those """
    score = request.json['score']
    session['nplay'] = session.get('nplay', 0) + 1
    session['highest'] = max(score, session.get('highest', 0))

    return jsonify({'nplay': session.get('nplay', 0),
                    'highest': session.get('highest', 0)
                   })

#!/usr/local/bin/python
from stockfish import Stockfish
from flask import Flask, json, request, jsonify

stockfish_easy = Stockfish()
stockfish_medium = Stockfish(depth=6)
stockfish_difficult = Stockfish(parameters={"MultiPV": 3},depth=20)

api = Flask(__name__)

@api.route('/move', methods=['POST'])

def post_move():
    fen = ""
    if "fen" in request.form:
        fen = request.form['fen']
    else:
        return jsonify(status='error',message='No fen provided')
    level = ""
    if "level" in request.form:
        level = request.form['level']
    #stockfish.set_fen_position("N7/P3pk1p/3p2p1/r4p2/8/4b2B/4P1KP/1R6 w - - 0 34")
    if level == 'difficult':
        stockfish_difficult.set_fen_position(fen)
        move = stockfish_difficult.get_best_move()
    elif level == 'medium':
        stockfish_medium.set_fen_position(fen)
        move = stockfish_medium.get_best_move()
    else:
        stockfish_easy.set_fen_position(fen)
        move = stockfish_easy.get_best_move()
        level="easy"

    return jsonify(status='ok',move=move, fen=fen, level=level)


@api.route("/hello", methods=['GET'])

def get_hello():
    return "Hello World\n"


if __name__ == '__main__':
    api.run()


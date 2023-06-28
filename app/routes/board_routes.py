from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card 
from app.models.board import Board
from app import db
import os
import requests

board_bp = Blueprint("board_bp", __name__, url_prefix="/board")

'''
Board CRUD Routes
'''
# I checked this post route - works!
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_board = Board(title = request_body["title"], owner = request_body["owner"])
                    
    db.session.add(new_board)
    db.session.commit()

    return make_response({"board": new_board.response_dict()}, 201)

# I checked this get route - works!
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append({
            "board_id": board.board_id,
            "title": board.title})
    return jsonify(board_response)

# I checked this get route - works!
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):    
    board = Board.query.get(board_id)
    if board is None:
        return make_response({"message" :f"Board {board_id} not found"}, 404)
    return make_response({"board": board.response_dict(), "card": board.return_cards()}, 200)

# tested - works!
@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response({'message': f'Board {board_id} not found'}, 404)

    form_data = request.get_json()
    board.title = form_data["title"]

    db.session.commit()
    return make_response({"board": {"id": board.board_id, "title": board.title}}, 200)

# I checked this delete route - works!
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response({'message': f'Board {board_id} not found'}, 404)
    
    db.session.delete(board)
    db.session.commit()

    return make_response({'details' : f"Board {board_id} {board.title} successfully deleted"})

# I checked this get route - works - returned an empty array for cards!
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_for_board(board_id):
    board = Board.query.get(board_id)
    
    if board is None:
        return make_response({'message': f'Goal {board_id} not found'}, 404)
    cards = Card.query.join(Board).filter(Card.board_id == board_id).all()
    card_list = []
    if cards:
        for card in cards:
            card_list.append(card.response_dict())

    if request.method == "GET":
        return make_response({
                "board_id": board.board_id,
                "title": board.title,
                "cards": card_list 
        }, 200)

def slack_message_card(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    params = {
        'channel': "majj-inspiration-board",
        'text': message
    }
    print("sending message")
    message = requests.post(url, data=params, headers=headers)
    return message.json()


# tested this - works!
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_board(board_id):
    board = Board.query.get(board_id)

    form_data = request.get_json()
    card = Card(message=form_data["message"])
    board.cards.append(card)
    
    slack_message_card(f"Congratulations! You've just posted a card! '{card.message}'!")

    db.session.commit()

    return make_response({
        "board_id": board.board_id, 
        "card_id": card.card_id,
        "message": card.message,
        "likes_count": card.likes_count
    }, 200)
from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card 
from app.models.board import Board
from app import db

board_bp = Blueprint("board_bp", __name__, url_prefix="/board")

'''
Board CRUD Routes
'''
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

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append({
            "board_id": board.board_id,
            "title": board.title})
    return jsonify(board_response)

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):    
    board = Board.query.get(board_id)
    if board is None:
        return make_response({"message" :f"Board {board_id} not found"}, 404)
    return make_response({"board": {"id": board.id, "title": board.title}}, 200)

@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response({'message': f'Board {board_id} not found'}, 404)

    form_data = request.get_json()
    board.title = form_data["title"]

    db.session.commit()
    return make_response({"board": {"id": board.id, "title": board.title}}, 200)

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response({'message': f'Board {board_id} not found'}, 404)
    
    db.session.delete(board)
    db.session.commit()

    return make_response({'details' : f'Board {board_id} "{board.title}" successfully deleted'})

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
    
@board_bp.route("/<board_id>/cards", methods=["POST"])
def post_cards_for_board(board_id):
        board = Board.query.get(board_id)
    
        if board is None:
            return make_response({'message': f'Board {board_id} not found'}, 404)
        cards = Card.query.join(Board).filter(Card.board_id == board_id).all()
        card_list = []
        if cards:
            for card in cards:
                card_list.append(card.response_dict())

        form_data = request.get_json()
        board.cards = []

        card_id = form_data["card_id"]
        for cards in card_id:
            card = Card.query.get(card_id)
            Board.cards.append(card)

        db.session.commit()

        return make_response({
            "board_id": board.board_id, 
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        }, 200)
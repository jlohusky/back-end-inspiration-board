from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
import os

def get_valid_card_by_id(model, id):
    try:
        id = int(id)
    except:
        abort(make_response({'details': 'Invalid data'}, 400))


card_bp = Blueprint('cards', __name__, url_prefix="/cards")

@card_bp.route('', methods=['GET'])
def get_all_cards():
    # Get all Cards
    cards = Card.query.all()

    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response), 200


@card_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    
    # To be able to read the request we need to use the .getj_son() method
    card_is_valid: Card = get_valid_card_by_id(Card, card_id)

    card_is_valid.likes_count += 1
    db.session.commit()

    return {card_is_valid.to_dict()}, 200

@card_bp.route("/<card_id>/unlike", methods=["PUT"])
def mark_task_as_incompleted(card_id):

    card_is_valid: Card = get_valid_card_by_id(Card, card_id)

    card_is_valid.likes_count -= 1

    db.session.commit()

    return {"card": card_is_valid.to_dict()}, 200


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_board(card_id):
    
    card_to_delete: Card = get_valid_card_by_id(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    message_card = card_to_delete.message

    return {"details": f'Card {card_id} "{message_card}" successfully deleted'}, 200

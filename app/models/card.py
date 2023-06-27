from app import db
from app.models.board import Board

class Card(db.Model):

    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)

    @classmethod
    def dict_for_post_method(cls, cards_details):

        result = cls(
            message=cards_details["message"],
            likes_count=0)
        return result
    
    def to_dict(self):
        return \
            {
                'id': self.card_id,
                'message': self.message,
                'likes_count': self.likes_count
            }
from app import db
from app.models.board import Board

class Card(db.Model):

    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)

<<<<<<< HEAD
    @classmethod
    def dict_for_post_method(cls, cards_details):

        result = cls(
            message=cards_details["message"],
            likes_count=0)
        return result
    
=======
>>>>>>> 82e662be0fe1264ae0736a9bad64c5d1a6857342
    def to_dict(self):
        return \
            {
                'id': self.card_id,
                'message': self.message,
<<<<<<< HEAD
                'likes_count': self.likes_count
=======
                'likes_count': self.likes_count,
                'board_id': self.board_id
>>>>>>> 82e662be0fe1264ae0736a9bad64c5d1a6857342
            }
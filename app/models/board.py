from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', backref='board')

    def return_cards(self):
        cards = [card.to_dict() for card in self.cards if self.board_id == card.board_id]
        return cards

    def response_dict(self):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
            }

        return board_dict 

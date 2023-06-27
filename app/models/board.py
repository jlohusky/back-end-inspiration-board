from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    card = db.relationship('Card', backref='board')

    def response_dict(self):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
            }

        return board_dict 

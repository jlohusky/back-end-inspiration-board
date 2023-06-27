from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    card = db.relationship('Card', backref='board')

    def response_dict(self):
        return 
    {
        "board_id": self.id,
        "title": self.title,
        "owner": self.owner
    }
    
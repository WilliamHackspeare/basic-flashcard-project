from app_core import db

class User(db.Model):
  username = db.Column(db.String,primary_key=True)
  password = db.Column(db.String,nullable=False)
  name = db.Column(db.String,nullable=False)
  decks = db.relationship('Deck', backref='user', lazy=True)

class Deck(db.Model):
  deck_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  deck_name = db.Column(db.String,nullable=False)
  last_date = db.Column(db.DateTime)
  last_score = db.Column(db.Float,default=0.0)
  average_score = db.Column(db.Float,default=0.0)
  num_of_cards = db.Column(db.Integer,default=0)
  username = db.Column(db.String,db.ForeignKey("user.username"),nullable=False)
  cards = db.relationship('Card', backref='deck', lazy=True)
  __table_args__ = (
    db.UniqueConstraint(
        deck_name, username,
        ),
    )

class Card(db.Model):
  card_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
  front = db.Column(db.String,nullable=False)
  back = db.Column(db.String,nullable=False)
  deck_id = db.Column(db.String,db.ForeignKey("deck.deck_id"),nullable=False)
  __table_args__ = (
    db.UniqueConstraint(
        front, deck_id,
        ),
    )

db.create_all()
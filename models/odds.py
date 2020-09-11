from app import db

class OddsModel(db.Model):
    __tablename__ = 'odds'

    odds_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer )
    details = db.Column(db.String)
    over_under = db.Column(db.DECIMAL)

    def __init__(self, game_id, details, over_under):
        self.game_id = game_id
        self.details = details
        self.over_under = over_under

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_game_id(cls, game_id):
        return cls.query.filter_by(game_id=game_id).first()

    def json(self):
        return {
            'odds_id': self.odds_id,
            'game_id': self.game_id,
            'details': self.details,
            'over_under': str(self.over_under)
        }


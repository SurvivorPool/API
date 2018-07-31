from app import db

class LeagueModel(db.Model):
    __tablename__ = 'leagues'

    league_id = db.Column(db.Integer, nullable=False, primary_key=True)
    league_name = db.Column(db.String(50), nullable=False)
    league_description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    teams = db.relationship("PlayerTeamModel", lazy="dynamic")

    def __init__(self, league_id, league_name, league_description, price):
        self.league_id = league_id
        self.league_name = league_name
        self.league_description = league_description
        self.price = price
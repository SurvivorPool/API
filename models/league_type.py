from enum import Enum
from app import db


class LeagueTypeModel(db.Model):
    __tablename__ = 'league_types'

    league_type_id = db.Column(db.Integer, primary_key=True)
    league_type_name = db.Column(db.String(30), unique=True)
    league_type_description = db.Column(db.String(500))

    def __init__(self, league_type_name, league_type_description):
        self.league_type_name = league_type_name
        self.league_type_description = league_type_description

    def upsert(self):
        db.session.add(self)
        db.session.commit()

class LeagueTypes(Enum):
    STANDARD = 1





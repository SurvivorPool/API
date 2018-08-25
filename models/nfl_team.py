from app import db


class nflTeamModel(db.Model):
    __tablename__ = 'nfl_teams'

    nfl_team_id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(10), nullable=False)
    city_state = db.Column(db.String(40), nullable=False)
    full_name = db.Column(db.String(70), nullable=False)
    nickname = db.Column(db.String(40), unique=True, nullable=False)
    conference = db.Column(db.String(5), nullable=False)
    division = db.Column(db.String(5), nullable=False)

    def __init__(self, nfl_team_id, abbreviation, city_state, full_name, nickname, conference, division):
        self.nfl_team_id = nfl_team_id
        self.abbreviation = abbreviation
        self.city_state = city_state
        self.full_name = full_name
        self.nickname = nickname
        self.conference = conference
        self.division = division

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_team_id(cls, nfl_team_id):
        return cls.query.filter_by(nfl_team_id=nfl_team_id).first()

    def json(self):
        return {
            'nfl_team_id': self.nfl_team_id,
            'abbreviation': self.abbreviation,
            'city_state': self.city_state,
            'full_name': self.full_name,
            'nickname': self.nickname,
            'conference': self.conference,
            'division': self.division
        }

    @classmethod
    def find_all_nfl_teams(cls):
        return cls.query.all()


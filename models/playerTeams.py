from app import db
from models.user import UserModel
from models.league import LeagueModel

class PlayerTeamModel(db.Model):
    __tablename__ = 'player_teams'

    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    league_id = db.Column(
        db.Integer,
        db.ForeignKey('leagues.league_id'),
        nullable=False
    )
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'))
    team_name = db.Column(db.String(20), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    has_paid = db.Column(db.Boolean, default=False)

    user = db.relationship('UserModel')
    league = db.relationship('LeagueModel')

    def __init__(self, user_id, league_id, team_name):
        self.user_id = user_id
        self.league_id = league_id
        self.team_name = team_name
        self.is_active = True
        self.has_paid = False

    def json(self):
        user = UserModel.find_by_user_id(self.user_id)
        league = LeagueModel.find_league_by_id(self.league_id)
        return {
            'team_id': self.team_id,
            'user_info': user.user_json(),
            'league_info': league.json_league_info(),
            'team_name': self.team_name,
            'is_active': self.is_active,
            'has_paid': self.has_paid
        }

    def upsert(self):
        db.session.add(self)        
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_team_id(cls, team_id):
        return cls.query.filter_by(team_id=team_id).first()

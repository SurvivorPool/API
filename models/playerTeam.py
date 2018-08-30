import app
from .game import GameModel
db = app.db


class PlayerTeamModel(db.Model):
    __tablename__ = 'player_teams'

    team_id = db.Column(db.Integer, primary_key=True, nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('leagues.league_id'), nullable=False)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'))
    team_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    has_paid = db.Column(db.Boolean, default=False)
    streak = db.Column(db.Integer, server_default='0', default=0, nullable=False)

    user = db.relationship('UserModel')
    league = db.relationship('LeagueModel')
    team_picks = db.relationship('PickModel')

    def __init__(self, user_id, league_id, team_name):
        self.user_id = user_id
        self.league_id = league_id
        self.team_name = team_name
        self.is_active = True
        self.has_paid = False
        self.streak = 0

    def json(self):
        current_week = GameModel.get_max_week()
        return {
            'team_id': self.team_id,
            'user_info': self.user.user_json(),
            'league_info': self.league.json_league_info(),
            'team_name': self.team_name,
            'is_active': self.is_active,
            'has_paid': self.has_paid,
            'current_pick': [
                pick.nfl_team_name for pick in self.team_picks
                if pick.week_num == current_week
            ],
            'pick_history': [pick.json_basic() for pick in self.team_picks if pick.week_num != current_week],
            'streak': self.streak,
            'current_week': current_week
        }

    def json_basic(self):
        return {
            'team_id': self.team_id,
            'user_info': self.user.user_json(),
            'team_name': self.team_name,
            'is_active': self.is_active,
            'has_paid': self.has_paid,
            'streak': self.streak
        }

    def json_for_user(self):
        current_week = GameModel.get_max_week()
        return {
            'team_id': self.team_id,
            'league_id': self.league_id,
            'team_name': self.team_name,
            'is_active': self.is_active,
            'has_paid': self.has_paid,
            'current_pick': [
                pick.nfl_team_name for pick in self.team_picks
                if pick.week_num == current_week],
            'pick_history': [pick.json_basic() for pick in self.team_picks if pick.week_num != current_week],
            'streak': self.streak,
            'current_week': current_week
        }

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def find_by_team_id(cls, team_id):
        return cls.query.filter_by(team_id=team_id).first()

    @classmethod
    def get_unique_leagues_for_user(cls, user_id):
        teams = cls.find_by_user_id(user_id)

        leagues = []

        for team in teams:
            leagues.append(team.league)
        league_set = set(leagues)
        return league_set

    @classmethod
    def get_active_teams_in_league(cls, league_id):
        return cls.query.filter_by(league_id=league_id, is_active=True)


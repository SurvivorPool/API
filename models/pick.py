from sqlalchemy import func
from sqlalchemy.sql import label
import app
import models.playerTeam as playerTeam
from models.game import GameModel

db = app.db


class PickModel(db.Model):
    __tablename__ = 'picks'

    pick_id = db.Column(db.Integer, nullable=False, primary_key=True)
    team_id = db.Column(
        db.Integer, db.ForeignKey('player_teams.team_id'), nullable=False)
    game_id = db.Column(
        db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    week_num = db.Column(db.Integer, nullable=False)
    nfl_team_name = db.Column(db.String(30), db.ForeignKey('nfl_teams.nickname'), nullable=False)

    player_team = db.relationship('PlayerTeamModel')
    nfl_team_info = db.relationship('NFLTeamModel')
    game = db.relationship('GameModel')

    def __init__(self, team_id, game_id, week_num, nfl_team_name):
        self.team_id = team_id
        self.game_id = game_id
        self.week_num = week_num
        self.nfl_team_name = nfl_team_name

    def json(self):
        return {
            'pick_id': self.pick_id,
            'team_info': self.player_team.json_basic(),
            'game_id': self.game_id,
            'week_num': self.week_num,
            'nfl_team_name': self.nfl_team_name
        }

    def json_basic(self):
        return {
            'pick_id': self.pick_id,
            'game_id': self.game_id,
            'week_num': self.week_num,
            'nfl_team_name': self.nfl_team_name
        }

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, pick_id):
        return cls.query.filter_by(pick_id=pick_id).first()

    @classmethod
    def find_team_picks(cls, team_id):
        return cls.query.filter_by(team_id=team_id).all()

    @classmethod
    def find_previous_team_picks(cls, team_id):
        return cls.query.filter(cls.team_id == team_id)

    @classmethod
    def is_duplicate_team_pick(cls, team_id, nfl_team_name):
        week_num = GameModel.get_max_week()
        prev_picks = cls.query.filter(cls.team_id == team_id,
                                      cls.nfl_team_name == nfl_team_name,
                                      cls.week_num < week_num).first()
        return prev_picks is not None

    @classmethod
    def current_week_pick_required(cls, team_id):
        team = playerTeam.PlayerTeamModel.find_by_team_id(team_id)
        if not team.is_active:
            return False

        week = GameModel.get_max_week()
        pick = cls.find_pick_by_week_and_team_id(week, team_id)

        return pick is None

    @classmethod
    def find_pick_by_week_and_team_id(cls, week_num, team_id):
        return cls.query.filter_by(team_id=team_id, week_num=week_num).first()

    @classmethod
    def find_previous_week_picks_for_league(cls, league_id):
        prev_week_num = GameModel.get_max_week() - 1
        return db.session.query(cls.nfl_team_name, label('count', func.count(cls.nfl_team_name))).filter_by(week_num=prev_week_num)\
            .join(cls.player_team).filter_by(league_id=league_id).group_by(cls.nfl_team_name).all()

    @classmethod
    def find_all_picks(cls):
        prev_week_num = GameModel.get_max_week() - 1
        return db.session.query(cls.nfl_team_name, label('count', func.count(cls.nfl_team_name))).filter_by(
            week_num=prev_week_num).group_by(cls.nfl_team_name).all()

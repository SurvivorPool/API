from datetime import datetime
from sqlalchemy.sql.expression import func
import app
db = app.db


class GameModel(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    home_team_name = db.Column(db.String(45))
    home_team_city_abbr = db.Column(db.String(10))
    home_team_score = db.Column(db.Integer, default=0)
    away_team_name = db.Column(db.String(45))
    away_team_city_abbr = db.Column(db.String(10))
    away_team_score = db.Column(db.Integer, default=0)
    day_of_week = db.Column(db.String(3))
    time = db.Column(db.String(5))
    game_date = db.Column(db.DateTime)
    quarter = db.Column(db.String(3))
    week = db.Column(db.Integer)

    def __init__(self, game_id, home_team_name, home_team_city_abbr,
                 home_team_score, away_team_name, away_team_city_abbr,
                 away_team_score, day_of_week, time, game_date, quarter, week):
        self.game_id = game_id
        self.home_team_name = home_team_name
        self.home_team_city_abbr = home_team_city_abbr
        self.home_team_score = home_team_score
        self.away_team_name = away_team_name
        self.away_team_city_abbr = away_team_city_abbr
        self.away_team_score = away_team_score
        self.day_of_week = day_of_week
        self.time = time
        self.game_date = game_date
        self.quarter = quarter
        self.week = week

    def __repr__(self):
        return '<Game {}>'.format(self.game_id)

    @classmethod
    def find_by_game_id(cls, game_id):
        return cls.query.filter_by(game_id=game_id).first()

    def json(self):
        return {
            'game_id': self.game_id,
            'home_team_name': self.home_team_name,
            'home_team_city_abbr': self.home_team_city_abbr,
            'home_team_score': self.home_team_score or 0,
            'away_team_name': self.away_team_name,
            'away_team_city_abbr': self.away_team_city_abbr,
            'away_team_score': self.away_team_score or 0,
            'day_of_week': self.day_of_week,
            'time': self.time,
            'game_date': datetime.strftime(self.game_date, '%Y-%m-%d'),
            'quarter': self.quarter,
            'week': self.week
        }

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_max_week(cls):
        return db.session.query(func.max(cls.week)).scalar()

    @classmethod
    def get_games_by_week(cls, week):
        return cls.query.all()

    @classmethod
    def get_games_by_week_json(cls, week):
        return {
            'games': [game.json() for game in cls.query.filter_by(week=week)]
        }

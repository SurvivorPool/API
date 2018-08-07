from app import db
from models.playerTeams import PlayerTeamModel

class PickModel(db.Model):
    __tablename__ = 'picks'

    pick_id = db.Column(db.Integer, nullable=False,  primary_key=True)
    team_id = db.Column(
        db.Integer, db.ForeignKey('player_teams.team_id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    week_num = db.Column(db.Integer, nullable=False)
    nfl_team_name = db.Column(db.String(30), nullable=False)

    player_team = db.relationship('PlayerTeamModel' )

    def __init__(self, team_id, game_id, week_num, nfl_team_name):
        self.pick_id = 1
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

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, pick_id):
        return cls.query.filter_by(pick_id=pick_id).first()


    @classmethod
    def find_previous_team_picks(cls, team_id):
        return cls.query.filter_by(team_id=team_id)

    @classmethod
    def find_pick_by_week_and_team_id(cls, week_num, team_id):
        return cls.query.filter_by(team_id=team_id, week_num=week_num).first()

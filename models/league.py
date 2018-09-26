import app
from .game import GameModel
from .user import UserModel
from.league_type import LeagueTypes
from controllers.free_league_register import  FreeLeagueRegisterController
from controllers.standard_league_register import StandardLeagueRegisterController
db = app.db


class LeagueModel(db.Model):
    __tablename__ = 'leagues'

    league_id = db.Column(db.Integer, nullable=False, primary_key=True)
    league_name = db.Column(db.String(50), nullable=False)
    league_description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    league_type_id = db.Column(db.Integer, db.ForeignKey('league_types.league_type_id'),
                               default=LeagueTypes.STANDARD.value, server_default=str(LeagueTypes.STANDARD.value))
    start_week = db.Column(db.Integer, nullable=False, default=1, server_default="1")
    completed = db.Column(db.Boolean, nullable=False, default=False, server_default="false")
    teams = db.relationship("PlayerTeamModel", order_by="desc(PlayerTeamModel.is_active), desc(PlayerTeamModel.streak)")
    league_type = db.relationship("LeagueTypeModel")

    def __init__(self, league_name, league_description, price):
        self.league_name = league_name
        self.league_description = league_description
        self.price = price

    def json(self):
        json = self.json_league_info()
        json['current_week'] = GameModel.get_max_week()
        json['teams'] = [team.json_basic() for team in self.teams]
        return json

    def json_league_info(self):
        price = self.price / 100
        return {
            'league_id': self.league_id,
            'league_name': self.league_name,
            'league_type': self.league_type.league_type_name,
            'league_description': self.league_description,
            'price': "{:,.2f}".format(price),
            'pot': price * len(self.teams),
            'start_week': self.start_week,
            'completed': self.completed
        }

    def json_league_info_with_active(self, user_id):
        json = self.json_league_info()
        json['is_active'] = self.get_active_status(user_id)
        return json


    def get_active_status(self, user_id):
        if self.league_type.league_type_name == LeagueTypes.STANDARD.name:
            return StandardLeagueRegisterController.full_validate(self)
        elif self.league_type.league_type_name == LeagueTypes.FREE.name:
            user = UserModel.find_by_user_id(user_id)
            return FreeLeagueRegisterController.full_validate(self, user)

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_league_by_id(cls, league_id):
        return cls.query.filter_by(league_id=league_id).first()

    @classmethod
    def find_all_leagues(cls):
        return cls.query.order_by(cls.price).all()

    @classmethod
    def find_all_started_leagues(cls, current_week):
        return cls.query.filter(cls.start_week <= current_week).all()

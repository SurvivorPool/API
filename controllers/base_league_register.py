from models.game import GameModel

class BaseLeagueRegisterController:

    @classmethod
    def validate(cls, league):
        return True #GameModel.week_has_unfinished_games(league.start_week)

    @classmethod
    def register(cls, team):
        team.upsert()
        return team.json(), 201


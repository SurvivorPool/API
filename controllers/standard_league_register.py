from .base_league_register import BaseLeagueRegisterController


class StandardLeagueRegisterController(BaseLeagueRegisterController):

    @classmethod
    def register(cls, league, team):
        if not super().validate(league):
            return {'message': 'Cannot join league. No games left in pregame.'.format(league.start_week)}, 401

        return super().register(team)

    @classmethod
    def validate(cls, league):
        return super().validate(league)
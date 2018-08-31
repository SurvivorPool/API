from .base_league_register import BaseLeagueRegisterController


class FreeLeagueRegisterController(BaseLeagueRegisterController):

    @classmethod
    def register(cls, league, team, user):

        if not cls.validate(league, user):
            return {'message': 'Cannot join league. Free leagues are 1 team per user.'}, 401

        if not super().validate(league):
            return {'message': 'Cannot join league. No games left in pregame.'.format(league.start_week)}, 401

        return super().register(team)

    @classmethod
    def full_validate(cls, league, team):
        return super().validate(league) and cls.validate(league, team)

    @classmethod
    def validate(cls, league, user):
        return len([player_team for player_team in user.teams if player_team.league_id == league.league_id]) == 0



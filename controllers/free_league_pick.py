from .standard_league_pick import StandardLeaguePickController


class FreeLeaguePickController(StandardLeaguePickController):

    @classmethod
    def validate_pick(cls, data):
        return super().validate_pick(data)


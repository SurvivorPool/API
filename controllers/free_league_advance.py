from .standard_league_advance import StandardLeagueAdvanceController


class FreeLeagueAdvanceController(StandardLeagueAdvanceController):

    @classmethod
    def validate_pick(cls, data):
        return super().advance_week(data)


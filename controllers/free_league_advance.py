from .standard_league_advance import StandardLeagueAdvanceController


class FreeLeagueAdvanceController(StandardLeagueAdvanceController):

    @classmethod
    def advance_week(cls, league):
        return super().advance_week(league)


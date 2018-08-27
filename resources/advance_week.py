from flask_restplus import Resource
from models.league import LeagueModel, LeagueTypes
from models.game import GameModel
from controllers import StandardLeagueAdvanceController


class AdvanceWeek(Resource):

    def put(self):
        #TODO:UNCOMMENT
        week_num = GameModel.get_max_week()
        # if GameModel.week_has_unfinished_games(week_num):
        #     return {'message': 'Not all games finished'}

        all_leagues = LeagueModel.find_all_leagues()
        for league in all_leagues:
            if league.league_type.league_type_name == LeagueTypes.STANDARD.name:
                return StandardLeagueAdvanceController.advance_week(league)
            else:
                return {'message': 'Advancing for this league type has not been implemented'}
        return {'message': 'No Leagues found'}



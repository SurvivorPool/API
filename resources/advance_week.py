from flask_restplus import Resource
from models.league import LeagueModel, LeagueTypes
from models.game import GameModel
from controllers import StandardLeagueAdvanceController, FreeLeagueAdvanceController
import authentication

class AdvanceWeek(Resource):

    @authentication.admin_required
    def put(self):
        week_num = GameModel.get_max_week()
        # if GameModel.week_has_unfinished_games(week_num):
        #     return {'message': 'Not all games finished'}

        all_leagues = LeagueModel.find_all_started_leagues(week_num)
        deactivated_teams = []
        advancing_teams = []

        for league in all_leagues:
            if league.league_type.league_type_name == LeagueTypes.STANDARD.name:
                teams_dict = StandardLeagueAdvanceController.advance_week(league)
            elif league.league_type.league_type_name == LeagueTypes.FREE.name:
                teams_dict = FreeLeagueAdvanceController.advance_week(league)
            else:
                raise NotImplementedError

            deactivated_teams += (teams_dict['deactivated_teams'])
            advancing_teams += (teams_dict['advancing_teams'])

        return {
            'deactivated_teams': [team.json_advance_week() for team in deactivated_teams],
            'advancing_teams': [team.json_advance_week() for team in advancing_teams]
                }



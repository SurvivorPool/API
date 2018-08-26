from flask_restplus import Resource, reqparse
from models.league_type import LeagueTypes
import controllers
import authentication
import models
PlayerTeamModel = models.PlayerTeamModel

StandardLeaguePickController = controllers.StandardLeaguePickController


class Pick(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'team_id', type=int, required=True, help='team_id cannot be null')
    parser.add_argument(
        'nfl_team_name',
        type=str,
        required=True,
        help='nfl_team_name cannot be null')
    parser.add_argument(
        'game_id', type=int, required=True, help='game_id cannot be null')

    #@authentication.player_team_ownership_required_json_param
    def put(self):
        data = self.parser.parse_args()

        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        if team:
            league_type_id = team.league.league_type.league_type_id
            print(league_type_id)
            if league_type_id == LeagueTypes.STANDARD.value:
                return StandardLeaguePickController.validate_pick(data)
            else:
                raise NotImplementedError

        return {'error': 'error'}




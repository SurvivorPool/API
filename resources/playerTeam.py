from flask_restplus import Resource, reqparse, fields
from authentication \
    import player_team_ownership_required_url_param, \
    player_team_ownership_required_json_param, login_required, user_and_session_match_json_param

import app
from models.playerTeam import PlayerTeamModel
from models.league import LeagueModel
from models.league_type import LeagueTypes
from models.user import UserModel
from controllers import StandardLeagueRegisterController, FreeLeagueRegisterController
api = app.api


class PlayerTeam(Resource):
    player_team_swagger = api.model('PlayerTeam', {
        'team_id': fields.String,
    })

    @api.expect(player_team_swagger)
    @player_team_ownership_required_url_param
    def get(self, team_id):
        team = PlayerTeamModel.find_by_team_id(team_id)

        if team:
            return team.json(), 200
        return {'message': 'Could not find a team with that id.'}, 404

    @user_and_session_match_json_param
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id', type=str, required=True, help='user_id cannot be null')
        parser.add_argument(
            'team_name',
            type=str,
            required=True,
            help='team_name cannot be null')
        parser.add_argument(
            'league_id', required=True, help='league_id cannot be null')
        parser.add_argument('team_id', type=int, required=False)

        data = parser.parse_args()

        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        if team is None:
            league = LeagueModel.find_league_by_id(data['league_id'])
            team = PlayerTeamModel(data['user_id'], data['league_id'],
                                   data['team_name'])
            league_type_name = league.league_type.league_type_name
            if league_type_name == LeagueTypes.STANDARD.name:
                return StandardLeagueRegisterController.register(league, team)
            elif league_type_name == LeagueTypes.FREE.name:
                user = UserModel.find_by_user_id(data['user_id'])
                return FreeLeagueRegisterController.register(league, team, user)
            else:
                return {'message': 'League type not yet implemented.'}, 402
        else:
            team.team_name = data['team_name']
            team.upsert()

        return team.json(), 201

    @login_required
    @player_team_ownership_required_json_param
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'team_id', type=int, required=True, help='team_id cannot be null')

        data = parser.parse_args()

        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        try:
            team.delete()
        except:
            return {
                'message': 'An error occurred while deleting the team'
            }, 500

        return {'message': 'Team deleted'}, 200


class PlayerTeamRegistrationStatus(Resource):

    @login_required
    def get(self, league_id, user_id):
        league = LeagueModel.find_league_by_id(league_id)
        user = UserModel.find_by_user_id(user_id)

        if not league:
            return {'message': 'League not found.'}, 404
        if not user:
            return {'message': 'User not found'}, 404

        league_type_name = league.league_type.league_type_name

        if league_type_name == LeagueTypes.STANDARD.name:
            return {'league_open': StandardLeagueRegisterController.validate(league)}, 200
        elif league_type_name == LeagueTypes.FREE.name:
            return {'league_open': FreeLeagueRegisterController.full_validate(league, user)}, 200
        else:
            return {'message': 'League type not yet implemented.'}, 402






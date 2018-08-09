from flask_restplus import Resource, reqparse, fields
from models.playerTeams import PlayerTeamModel
from app import api

class PlayerTeam(Resource):
    player_team_swagger = api.model('PlayerTeam', {
        'team_id': fields.String,
    })

    @api.expect(player_team_swagger)
    def get(self, team_id):
        team = PlayerTeamModel.find_by_team_id(team_id)

        if not team is None:
            return team.json(), 200
        return {'message': 'Could not find a team with that id.'}, 404

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id', type=str, required=True, help='user_id cannot be null')
        parser.add_argument(
            'team_name', type=str, required=True, help='team_name cannot be null'
        )
        parser.add_argument('league_id', required=True, help='league_id cannot be null')
        parser.add_argument('team_id', type=int, required=False)

        data = parser.parse_args()

        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        if team is None:
            team = PlayerTeamModel(data['user_id'], data['league_id'], data['team_name'])
        else:
            team.team_name = data['team_name']

        try:
            team.upsert()
        except:
            return {'message': 'An error occurred inserting the player team'}, 500

        return team.json(), 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('team_id', type=int, required=True, help='team_id cannot be null')

        data = parser.parse_args()

        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        try:
            team.delete()
        except:
            return { 'message': 'An error occurred while deleting the team'}, 500

        return { 'message': 'Team deleted'}, 200

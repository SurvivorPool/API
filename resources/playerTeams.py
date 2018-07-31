from flask_restful import Resource, reqparse
from models.playerTeams import PlayerTeamModel

class PlayerTeam(Resource):
    def get(self, team_id):
        team = PlayerTeamModel.find_by_team_id(team_id)
        return team.json(), 200
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id', type=str, required=True, help='user_id cannot be null')
        parser.add_argument(
            'team_name', type=str, required=True, help='team_name cannot be null'
        )

        data = parser.parse_args()

        team = PlayerTeamModel(data['user_id'], data['team_name'])
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


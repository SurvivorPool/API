from flask_restplus import Resource, reqparse
from authentication import admin_required
from models.pick import PickModel
from models.playerTeam import PlayerTeamModel


class AdminTeam(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'team_id', type=str, required=True, help='team_id cannot be null')

    @admin_required
    def put(self):
        self.parser.add_argument(
            'has_paid', type=bool, required=True, help='has_paid cannot be null')
        self.parser.add_argument(
            'is_active', type=bool, required=True, help='is_active cannot be null')

        data = self.parser.parse_args()
        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        if not team:
            return {'message': 'Team with that team_id cannot be found.'}, 401

        team.has_paid = data['has_paid']
        team.is_active = data['is_active']

        team.upsert()

        return team.json()

    @admin_required
    def delete(self):
        data = self.parser.parse_args()
        team = PlayerTeamModel.find_by_team_id(data['team_id'])

        if not team:
            return {'message': 'Team with that team_id cannot be found.'}, 401

        picks = PickModel.find_team_picks(data['team_id'])

        if picks is not None:
            return {'message': 'Cannot delete this team. Picks are associated to it still.'}, 500

        team.delete()

        return {'message': 'team was successfully deleted.'}


class AdminTeams(Resource):

    @admin_required
    def get(self):
        teams = PlayerTeamModel.get_all_player_teams()

        return {
            'teams': [team.json() for team in teams]
        }



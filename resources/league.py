from flask_restplus import Resource, reqparse, fields
from authentication import login_required, admin_required

import app
import models

LeagueModel = models.LeagueModel
PlayerTeamModel = models.PlayerTeamModel
api = app.api


class League(Resource):
    league_swagger = api.model('League', {
        'league_id': fields.String,
    })
    parser = reqparse.RequestParser()
    parser.add_argument('league_id', type=int)
    parser.add_argument(
        'league_name',
        type=str,
        required=True,
        help='league_name cannot be null')
    parser.add_argument(
        'league_description',
        type=str,
        required=True,
        help='league_description cannot be null')
    parser.add_argument(
        'price', type=int, required=True, help='price cannot be null')

    @api.expect(league_swagger)
    @login_required
    def get(self, league_id):
        league = LeagueModel.find_league_by_id(league_id)
        if not league is None:
            return league.json()
        return {'message': 'League not found'}, 404

    @api.expect(parser)
    @admin_required
    def put(self):
        data = self.parser.parse_args()
        league = LeagueModel.find_league_by_id(data['league_id'])

        if league is None:
            league = LeagueModel(data['league_name'],
                                 data['league_description'], data['price'])
        else:
            league.league_name = data['league_name']
            league.league_description = data['league_description']
            league.price = data['price']

        try:
            league.upsert()
            return league.json()
        except:
            return {'message': 'An error occurred upserting the league'}, 500


class LeaguesByUser(Resource):
    leagues_by_user_swagger = api.model('UserLeagues', {
        'user_id': fields.String,
    })

    @api.expect(leagues_by_user_swagger)
    @login_required
    def get(self, user_id):
        leagueSet = PlayerTeamModel.get_unique_leagues_for_user(user_id)
        return {
            'user_leagues':
            [league.json_league_info() for league in leagueSet]
        }


class LeaguesList(Resource):
    @login_required
    def get(self):
        leagues = LeagueModel.find_all_leagues()
        return {'leagues': [league.json_league_info() for league in leagues]}

from flask_restful import Resource, reqparse
from models.league import LeagueModel

class League(Resource):
    def get(self, league_id):
        league = LeagueModel.find_league_by_id(league_id)
        if not league is None:
            return league.json()
        return {'message': 'League not found'}, 404

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('league_id', type=int)
        parser.add_argument(
            'league_name',
            type=str,
            required=True,
            help='league_name cannot be null')
        parser.add_argument('league_description', type=str, required=True, help='league_description cannot be null')
        parser.add_argument('price', type=int, required=True, help='price cannot be null')

        data = parser.parse_args()

        league = LeagueModel.find_league_by_id(data['league_id'])

        if league is None:
            league = LeagueModel(data['league_name'], data['league_description'], data['price'])
        else:
            league.league_name = data['league_name']
            league.league_description = data['league_description']
            league.price = data['price']
            
        try:
            league.upsert()
            return league.json()
        except:
            return {'message': 'An error occurred upserting the league'}, 500


        

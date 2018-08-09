from flask_restful import Resource, reqparse
from models.user import UserModel
from models.playerTeams import PlayerTeamModel
from models.league import LeagueModel

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)
        return user.json()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'user_id',
            type=str,
            required=True,
            help='user_id cannot be null')

        parser.add_argument(
            'full_name',
            type=str,
            required=True,
            help='full_name cannot be null')

        parser.add_argument(
            'email',
            type=str,
            required=True,
            help='email cannot be null')

        parser.add_argument(
            'picture_url',
            type=str)
        
        data = parser.parse_args()
        user = UserModel(data['user_id'], data['full_name'], data['email'], data['picture_url'])

        try:
            user.upsert()
        except:
            return { 'message': 'An error occurred inserting the user'}, 500
        
        return user.json(), 201

class UserExistence(Resource):
    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)
        return True if user else False


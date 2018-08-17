from flask_restplus import Resource, reqparse, fields
import app
import models

api = app.api
UserModel = models.UserModel
PlayerTeamModel = models.PlayerTeamModel
LeagueModel = models.LeagueModel

user_swagger = api.model('User', {
    'user_id': fields.String,
})


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'user_id', type=str, required=True, help='user_id cannot be null')

    parser.add_argument(
        'full_name', type=str, required=True, help='full_name cannot be null')

    parser.add_argument(
        'email', type=str, required=True, help='email cannot be null')

    parser.add_argument('picture_url', type=str)

    @api.expect(user_swagger)
    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)
        return user.json()

    @api.expect(parser)
    def post(self):
        data = self.parser.parse_args()
        user = UserModel(data['user_id'], data['full_name'], data['email'],
                         data['picture_url'])

        try:
            user.upsert()
        except:
            return {'message': 'An error occurred inserting the user'}, 500

        return user.json(), 201


class UserExistence(Resource):
    @api.expect(user_swagger)
    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)
        exists = True if user else False
        return {'exists': exists}, 200

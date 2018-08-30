from flask_restplus import Resource, reqparse, fields
import app
from models.user import UserModel
import authentication

api = app.api
user_swagger = api.model('User', {
    'user_id': fields.String,
})


class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'user_id', type=str, required=True, help='user_id cannot be null')

    @api.expect(user_swagger)
    @authentication.user_and_session_match_url_param
    def get(self, user_id):
        user = UserModel.find_by_user_id(user_id)

        if user:
            return user.json()

        return {'message': 'cannot find user'}, 401

    @authentication.user_and_session_match_json_param
    def put(self):
        self.parser.add_argument('receive_notifications', type=bool)
        data = self.parser.parse_args()
        user = UserModel.find_by_user_id(data['user_id'])

        if user is None:
            return {'message': 'User not found.'}, 401

        if not data['receive_notifications'] is None:
            user.receive_notifications = data['receive_notifications']

        try:
            user.upsert()

        except Exception as a:
            print(a)
            return {'message': 'An error occured updating the user'}, 500

        return user.json_user_owner_basic()


    @api.expect(parser)
    def post(self):

        self.parser.add_argument(
            'full_name', type=str, required=True, help='full_name cannot be null')

        self.parser.add_argument(
            'email', type=str, required=True, help='email cannot be null')

        self.parser.add_argument('picture_url', type=str)

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


class AdminUsers(Resource):

    @authentication.admin_required
    def get(self):
        users = UserModel.get_all_users()
        return {
            'users': [user.json() for user in users]
        }

from datetime import datetime
from flask_restplus import Resource, reqparse
from models.user_message import UserMessageModel
from authentication import user_and_session_match_url_param, admin_required
from models.user import UserModel

class UserMessage(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    @user_and_session_match_url_param
    def get(self, user_id):
        messages = UserMessageModel.find_unread_messages_by_user_id(user_id)

        return {'messages': [return_message.json() for return_message in messages]}, 200

    @user_and_session_match_url_param
    def put(self, user_id):
        self.parser.add_argument('message_id', type=int, required=True, help='message_id cannot be null')

        self.parser.add_argument(
            'read', type=bool, required=True, help='read cannot be null')
        data = self.parser.parse_args()
        print(user_id)
        message = UserMessageModel.find_by_message_id(data['message_id'])

        message.read = data['read']
        message.read_date = datetime.utcnow() if message.read else None

        message.upsert()

        return message.json()


class AdminUserMessage(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        'user_ids', type=str, required=True, help='user_ids cannot be null', action="split")
    parser.add_argument('all_users', type=bool, required=True, help='all_users bool is required.')

    @admin_required
    def put(self):
        data = self.parser.parse_args()

        if data['all_users']:
            users = UserModel.get_all_users()
            user_ids = [user.user_id for user in users]
        else:
            user_ids = data.user_ids

        messages = []
        for user_id in user_ids:
            message = UserMessageModel('new message', 1, datetime.utcnow(), user_id)
            message.upsert()
            messages.append(message)

        return {'messages': [return_message.json() for return_message in messages]}, 200


class AdminUserMessages(Resource):

    def get(self):
        messages = UserMessageModel.get_all_messages()
        return {'messages': [message.json() for message in messages]}







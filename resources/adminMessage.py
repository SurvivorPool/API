from flask_restplus import Resource, reqparse, fields
import models

AdminMessageModel = models.AdminMessageModel


class AdminMessage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('message_id', type=int)
    parser.add_argument(
        'user_id', type=str, required=True, help='user_id cannot be null')
    parser.add_argument(
        'message_text',
        type=str,
        required=True,
        help='message_text cannot be null')
    parser.add_argument(
        'show_message', type=bool, help='show_message cannot be null')
    parser.add_argument(
        'message_type',
        type=str,
        required=True,
        help='message_type cannot be null')

    def get(self, message_id):
        message = AdminMessageModel.find_message_by_id(message_id)
        return message.json()

    def put(self):
        data = self.parser.parse_args()
        message = AdminMessageModel.find_message_by_id(data['message_id'])

        if message is None:
            message = AdminMessageModel(data['user_id'], data['message_text'],
                                        data['show_message'],
                                        data['message_type'])
        else:
            message.user_id = data['user_id']
            message.message_text = data['message_text']
            message.show_message = data['show_message']
            message.message_type = data['message_type']

        try:
            message.upsert()
            return {'message': message.json()}, 200
        except:
            return {'message': 'Unable to save message'}, 500


class AdminMessages(Resource):
    def get(self):
        messages = AdminMessageModel.find_all_active_messages()
        return {'messages': [message.json() for message in messages]}

from datetime import datetime
from app import db
from .user_message_type import UserMessageTypes


class UserMessageModel(db.Model):
    __tablename__ = 'user_messages'

    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(500), nullable=False)
    message_type_id = db.Column(db.Integer, db.ForeignKey('user_message_types.message_type_id'),
                             default=UserMessageTypes.DEFAULT.value, server_default=str(UserMessageTypes.DEFAULT.value))
    create_date = db.Column(db.DateTime)
    read = db.Column(db.Boolean, default=False, server_default="False", nullable=False)
    read_date = db.Column(db.DateTime)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'))

    message_type = db.relationship("UserMessageTypeModel")
    user = db.relationship('UserModel')

    def __init__(self, message_text, message_type_id, create_date, user_id):
        self.message_text = message_text
        self.message_type_id = message_type_id
        self.create_date = create_date
        self.user_id = user_id

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'message_id': self.message_id,
            'message_text': self.message_text,
            'message_type': self.message_type.message_type,
            'create_date': datetime.strftime(self.create_date, "%Y/%m/%d %I:%MM %p"),
            'read': self.read,
            'read_date': datetime.strftime(self.read_date, "%Y/%m/%d %I:%MM %p") if self.read else None,
            'user': self.user.json_user_owner_basic()
        }

    @classmethod
    def find_unread_messages_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, read=False).order_by(cls.message_id).all()

    @classmethod
    def find_by_message_id(cls, message_id):
        return cls.query.filter_by(message_id=message_id).first()

    @classmethod
    def get_all_messages(cls):
        return cls.query.all()






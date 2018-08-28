from enum import Enum
from app import db


class UserMessageTypeModel(db.Model):
    __tablename__ = 'user_message_types'

    message_type_id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.String(30))

    def __init__(self, message_type):
        self.message_type = message_type

    def upsert(self):
        db.session.add(self)
        db.session.commit()


class UserMessageTypes(Enum):
    DEFAULT = 1

from app import db
from .user_message_type import UserMessageTypes


class UserMessageModel(db.Model):
    __tablename__ = 'user_messages'

    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(500), nullable=False)
    message_type_id = db.Column(db.Integer, db.ForeignKey('league_types.league_type_id'),
                             default=UserMessageTypes.DEFAULT.value, server_default=str(UserMessageTypes.DEFAULT.value))
    create_date = db.Column(db.DateTime)
    read = db.Column(db.Boolean, default=False, server_default="False", nullable=False)
    read_date = db.Column(db.DateTime)

    message_type = db.relationship("UserMessageTypeModel")

    def __init__(self, message_text, message_type_id, create_date, read, read_date):
        self.message_text = message_text
        self.message_type_id = message_type_id
        self.create_date = create_date
        self.read = read
        self.read_date = read_date

    def upsert(self):
        db.session.add(self)
        db.session.commit()








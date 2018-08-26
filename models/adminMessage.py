import app
db = app.db


class AdminMessageModel(db.Model):
    __tablename__ = 'admin_messages'

    message_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(45), db.ForeignKey('users.user_id'))
    message_text = db.Column(db.String(500), nullable=False)
    show_message = db.Column(db.Boolean, default=True)
    message_type = db.Column(db.String(25), nullable=False)

    def __init__(self, user_id, message_text, show_message, message_type):
        self.user_id = user_id
        self.message_text = message_text
        self.show_message = show_message
        self.message_type = message_type

    def json(self):
        return {
            'message_id': self.message_id,
            'message_text': self.message_text,
            'show_message': self.show_message,
            'message_type': self.message_type
        }

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all_active_messages(cls):
        return cls.query.filter_by(show_message=True)

    @classmethod
    def find_message_by_id(cls, message_id):
        return cls.query.filter_by(message_id=message_id).first()


from app import db

class PickModel(db.Model):
    _tablename__ = 'picks'

    pick_id = db.Column(db.Integer, required=True, primary_key=True)
    week_num = db.Column(db.Integer, required=True)
    
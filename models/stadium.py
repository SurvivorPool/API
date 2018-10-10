from app import db


class StadiumModel(db.Model):
    __tablename__ = 'stadiums'

    stadium_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), nullable=False)
    stadium_name = db.Column(db.String(100), nullable=False)
    stadium_state = db.Column(db.String(5), nullable=True)
    roof_type = db.Column(db.String(40), nullable=False)

    def __init__(self, stadium_id, city, stadium_name, stadium_state, roof_type):
        self.stadium_id = stadium_id
        self.city = city
        self.stadium_name = stadium_name
        self.stadium_state = stadium_state
        self.roof_type = roof_type

    @classmethod
    def find_by_id(cls, stadium_id):
        return cls.query.filter_by(stadium_id=stadium_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'stadium_id': self.stadium_id,
            'city': self.city,
            'stadium_name': self.stadium_name,
            'state': self.stadium_state,
            'roof_type': self.roof_type
        }


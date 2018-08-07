from flask_restful import Resource, reqparse
from models.pick import PickModel

class Pick(Resource):

    def get(self):
        pick = PickModel.find_by_id(1)
        return pick.json(), 200

    def put(self):
        pick = PickModel(16, 57505, 1, 'Buccaneers')
        
        try:
            pick.upsert()
        except:
            return {'message': 'pick could not be made.'}, 500
        
        return pick.json(), 200



class PickHistory(Resource):

    def get(self):
        pass

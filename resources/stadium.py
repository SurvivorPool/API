from flask_restplus import Resource
from controllers.stadium import StadiumController
from authentication import admin_required


class Stadium(Resource):
    def put(self):
        print("HERE HERE HER HER")
        return self.populate_stadiums()

    #admin_required
    def populate_stadiums(self):
        print("HERE")
        return StadiumController.populate_stadiums()
from flask_restplus import Resource
from controllers.nfl_team import NFLTeamController
from authentication import admin_required


class NFLTeam(Resource):

    def put(self):
        return self.populate_teams()

    @admin_required
    def populate_teams(self):
        return NFLTeamController.populate_teams()
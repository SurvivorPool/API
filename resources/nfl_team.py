from flask_restplus import Resource
from controllers.nfl_team import NFLTeamController


class nflTeam(Resource):

    def put(self):
        return self.populate_teams()

    def populate_teams(cls):
        return NFLTeamController.populate_teams()
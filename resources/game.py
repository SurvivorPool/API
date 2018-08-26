from flask_restplus import Resource, fields
import app
from controllers import GameController
import authentication


class GamesList(Resource):

    @authentication.login_required
    def get(self):
        return GameController.update_games()


class AdminGames(Resource):
    @authentication.admin_required
    def put(self):
        return GameController.populate_games()

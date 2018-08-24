from flask_restplus import Resource, fields
import app
from controllers import GameController
import authentication

api = app.api


class GamesList(Resource):
    game_swagger = api.model('Game', {
        'weekNum': fields.String,
    })

    @api.expect(game_swagger)
    #@authentication.login_required
    def get(self, weekNum):
        return GameController.populate_games()#GameController.update_games(weekNum)


class AdminGames(Resource):
    @authentication.admin_required
    def put(self):
        return {}#GameController.populate_games()

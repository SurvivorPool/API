from flask_restplus import Resource, fields
from controllers.game import GameController
import app
api = app.api


class GamesList(Resource):
    game_swagger = api.model('Game', {
        'weekNum': fields.String,
    })

    @api.expect(game_swagger)
    def get(self, weekNum):
        return GameController.update_games(weekNum)

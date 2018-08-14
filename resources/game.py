from flask_restplus import Resource, fields
from models.game import GameModel
from controllers.game import GameController
from app import api


class GamesList(Resource):
    game_swagger = api.model('Game', {
        'weekNum': fields.String,
    })

    @api.expect(game_swagger)
    def get(self, weekNum):
        return GameController.update_games(weekNum)

from flask_restplus import Resource, fields
import app
import controllers

api = app.api
GameController = controllers.GameController


class GamesList(Resource):
    game_swagger = api.model('Game', {
        'weekNum': fields.String,
    })

    @api.expect(game_swagger)
    def get(self, weekNum):
        return GameController.update_games(weekNum)

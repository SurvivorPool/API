from flask_restplus import Resource, fields
import app
import controllers
import authentication

api = app.api
GameController = controllers.GameController


class GamesList(Resource):
    game_swagger = api.model('Game', {
        'weekNum': fields.String,
    })

    @api.expect(game_swagger)
    @authentication.login_required
    def get(self, weekNum):
        return GameController.update_games(weekNum)

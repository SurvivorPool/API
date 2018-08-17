from flask_restplus import Resource, reqparse

import models
import controllers
PickModel = models.PickModel
GameModel = models.GameModel
GameController = controllers.GameController


class Pick(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'team_id', type=int, required=True, help='team_id cannot be null')
    parser.add_argument(
        'nfl_team_name',
        type=str,
        required=True,
        help='nfl_team_name cannot be null')
    parser.add_argument(
        'game_id', type=int, required=True, help='game_id cannot be null')

    def put(self):
        data = self.parser.parse_args()
        week = GameModel.get_max_week()
        GameController.update_games(week)

        game = GameModel.find_by_game_id(data['game_id'])

        if game.quarter != 'P':
            return {
                'message':
                'This game has already started. Please try a different game.'
            }, 403

        if (PickModel.is_duplicate_team_pick(data['team_id'],
                                             data['nfl_team_name'])):
            return {'message': "You've already chosen this team."}, 401

        pick = PickModel.find_pick_by_week_and_team_id(week, data['team_id'])

        if pick is None:
            pick = PickModel(data['team_id'], data['game_id'], week,
                             data['nfl_team_name'])
        else:
            pick.game_id = data['game_id']
            pick.nfl_team_name = data['nfl_team_name']

        try:
            pick.upsert()
        except:
            return {'message': 'error upserting pick.'}, 500

        return {'pick': pick.json()}
from models.pick import PickModel
from models.game import GameModel
from .game import GameController


class StandardLeaguePickController:

    @classmethod
    def validate_pick(cls, data):

        week = GameModel.get_max_week()
        GameController.update_games()

        game = GameModel.find_by_game_id(data['game_id'])

        if game.quarter != 'P':
            return {
                       'message':
                           'This game has already started. Please try a different game.'
                   }, 403

        if data['nfl_team_name'] not in [game.home_team_name, game.away_team_name]:
            return {
                       'message':
                           'Team for selected pick is not a part of game with id {}.'.format(data['game_id'])
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

        return {
            'pick': pick.json()
        }

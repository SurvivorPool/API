from flask_restplus import Resource
from authentication import login_required
from models import PickModel


class StatisticsResource(Resource):

    @login_required
    def get(self, league_id):
        prev_week_picks = PickModel.find_previous_week_picks_for_league(league_id)
        all_picks = PickModel.find_all_picks()

        json = {
            'previous_week_picks_current_league': [
                {
                    'team_name': prev_week_pick.nfl_team_name,
                    'count': prev_week_pick.count
                }
                for prev_week_pick in prev_week_picks],
            'previous_week_picks_all_leagues': [
                {
                    'team_name': pick.nfl_team_name,
                    'count': pick.count
                }
                for pick in all_picks]

        }

        return json



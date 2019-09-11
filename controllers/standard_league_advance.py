from models.pick import PickModel
from models.game import GameModel
from models.playerTeam import PlayerTeamModel
from controllers.game import GameController
from config import Config
from app.email import send_email
from models.league_type import LeagueTypes


class StandardLeagueAdvanceController:

    @classmethod
    def advance_week(cls, league):
        #GameController.update_games()
        week_num = GameModel.get_max_week()

        active_teams = PlayerTeamModel.get_active_teams_in_league(league.league_id)

        losing_nfl_teams = GameController.get_losers_for_week(week_num)
        deactivated_teams = []
        advancing_teams = []
        for active_team in active_teams:
            pick = PickModel.find_pick_by_week_and_team_id(week_num, active_team.team_id)

            if pick is None:
                deactivated_teams.append(active_team)
            else:
                if pick.nfl_team_name in losing_nfl_teams:
                    active_team.is_active = False
                    deactivated_teams.append(active_team)
                else:
                    active_team.streak += 1
                    advancing_teams.append(active_team)
                active_team.upsert()

        for team in deactivated_teams:
            if team.user.receive_notifications:
                send_email("Sorry, you've been eliminated", Config.MAIL_USERNAME, team.user, team)

        return {
            'deactivated_teams': deactivated_teams,
            'advancing_teams': advancing_teams
        }





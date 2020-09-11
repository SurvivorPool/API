from datetime import timedelta

from models.game import GameModel
from controllers.stadium import StadiumController
from dateutil import parser
import calendar
import requests


class GameController:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    @classmethod
    def get_losers_for_week(cls, week_num):
        games = GameModel.get_games_by_week(week_num)

        losers = []
        for game in games:
            if game.home_team_score == game.away_team_score:
                losers.append(game.home_team_name)
                losers.append(game.away_team_name)
            elif game.home_team_score < game.away_team_score:
                losers.append(game.home_team_name)
            else:
                losers.append(game.away_team_name)

        return losers

    @classmethod
    def populate_games(cls):
        current_week = GameModel.get_max_week() or 0
        current_games = GameModel.get_games_by_week(current_week)
        StadiumController.upsert_stadiums()

        for game in current_games:
            if game.quarter != 'F' and game.quarter != 'FO':
                return {'message': 'not all games completed yet.'}, 401

        return cls.update_games()

    @classmethod
    def update_games(cls):
        rss_feed = requests.get(cls.nfl_endpoint)
        StadiumController.upsert_stadiums()

        json_data = rss_feed.json()

        week_info = json_data['week']
        week_num = week_info['number']

        print(week_num)
        events = json_data['events']

        for event in events:
            competitions = event['competitions']
            competition = competitions[0]
            teams = competition['competitors']

            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))
            status = event['status']
            type = status['type']
            has_started = not type['state'] == 'pre'

            game_model = GameModel.find_by_game_id(event['id'])

            if game_model is None:
                game_id = event['id']

                if 'name' not in home_team['team']:
                    home_team_name = home_team['team']['displayName']
                else:
                    home_team_name = home_team['team']['name']

                if 'name' not in away_team['team']:
                    away_team_name = away_team['team']['displayName']
                else:
                    away_team_name = away_team['team']['name']

                home_team_score = home_team['score'] or 0
                away_team_score = away_team['score'] or 0

                if status['period'] == 0 and type['state'] == 'pre':
                    quarter = 'P'
                elif type['state'] == 'post':
                    quarter = 'F'
                else:
                    quarter = status['period']

                quarter_time = status['displayClock']

                game_date = parser.parse(competition['startDate'])
                game_date_eastern = game_date - timedelta(hours=5)
                day_of_week = calendar.day_name[game_date_eastern.weekday()]
                site_id = competition['venue']['id']
                game_model = GameModel(game_id, home_team_name, home_team_score, away_team_name, away_team_score,
                                       day_of_week, game_date, quarter, quarter_time, site_id, week_num, has_started)

                game_model.upsert()
            else:
                game_model.home_team_score = home_team['score'] or 0
                game_model.away_team_score = away_team['score'] or 0

                if status['period'] == 0 and type['state'] == 'pre':
                    quarter = 'P'
                elif type['state'] == 'post':
                    quarter = 'F'
                else:
                    quarter = status['period']

                game_model.quarter = quarter
                game_model.quarter_time = status['displayClock']
                game_model.has_started = has_started
                game_date = parser.parse(competition['startDate'])

                game_date_eastern = game_date - timedelta(hours=5)
                day_of_week = calendar.day_name[game_date_eastern.weekday()]

                game_model.game_date = game_date
                game_model.day_of_week = day_of_week
                game_model.site_id = competition['venue']['id']
                game_model.upsert()

        return_games = GameModel.get_games_by_week(week_num)
        return {'games': [game.json() for game in return_games]}

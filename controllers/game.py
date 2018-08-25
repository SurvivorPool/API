from models.game import GameModel
from datetime import datetime
import time
import calendar
import requests
import json
import xml.etree.ElementTree as ET
import urllib.request


class GameController:

    nfl_endpoint = 'https://feeds.nfl.com/feeds-rs/scores.json'

    @classmethod
    def populate_games(cls):
        current_week = GameModel.get_max_week() or 0
        current_games = GameModel.get_games_by_week(current_week)

        # for game in current_games:
        #     if game.quarter != 'F' and game.quarter != 'FO':
        #         return {'message': 'not all games completed yet.'}, 401

        rss_feed = requests.get(cls.nfl_endpoint)

        json_data = rss_feed.json()

        week_num = json_data['week']
        games = json_data['gameScores']

        default_score_info = {'homeTeamScore': {'pointTotal': 0}, 'visitorTeamScore': {'pointTotal': 0},
                              'phase': 'PREGAME', 'time': '15:00'}

        for game in games:
            schedule_info = game['gameSchedule']
            score_info = game['score'] if game['score'] else default_score_info
            home_score_info = score_info['homeTeamScore']
            away_score_info = score_info['visitorTeamScore']
            home_team_info = schedule_info['homeTeam']
            away_team_info = schedule_info['visitorTeam']
            site_info = schedule_info['site']
            game_model = GameModel.find_by_game_id(schedule_info['gameKey'])

            if game_model is None:
                game_id = schedule_info['gameKey']
                home_team_name = home_team_info['nick']
                home_team_score = home_score_info['pointTotal'] or 0
                away_team_name = away_team_info['nick']
                away_team_score = away_score_info['pointTotal'] or 0

                quarter = score_info['phase'][0] if len(score_info['phase']) > 3  else score_info['phase']

                quarter_time = score_info['time']

                game_date = datetime.strptime(schedule_info['gameDate'], '%m/%d/%Y')
                game_time_24hr = time.strptime(schedule_info['gameTimeEastern'], "%H:%M:%S")
                game_time = time.strftime("%I:%M %p", game_time_24hr)

                day_of_week = calendar.day_name[game_date.weekday()]
                site_id = site_info['siteId']
                game_model = GameModel(game_id, home_team_name, home_team_score, away_team_name, away_team_score,
                                       day_of_week, game_time, game_date, quarter, quarter_time, site_id, week_num)
                game_model.upsert()
            else:
                game_model.home_team_score = home_score_info['pointTotal'] or 0
                game_model.away_team_score = away_score_info['pointTotal'] or 0
                game_model.quarter = score_info['phase'][0] if len(score_info['phase']) > 3 else score_info['phase']
                game_model.quarter_time = score_info['time']
                game_model.game_date = datetime.strptime(schedule_info['gameDate'], '%m/%d/%Y')
                game_time_24hr = time.strptime(schedule_info['gameTimeEastern'], "%H:%M:%S")
                game_model.game_time = time.strftime("%I:%M %p", game_time_24hr)
                game_model.day_of_week = calendar.day_name[game_model.game_date.weekday()]
                game_model.site_id = site_info['siteId']
                game_model.upsert()

        return_games = GameModel.get_games_by_week(week_num)
        return {'games': [game.json() for game in return_games]}


    @classmethod
    def populate_games_old(cls):
        currentWeek = GameModel.get_max_week() or 0
        currentGames = GameModel.get_games_by_week(currentWeek)

        for game in currentGames:
            if game.quarter != 'F' and game.quarter != 'FO':
                return {'message': 'not all games completed yet.'}, 401

        weekNum = currentWeek + 1
        return cls.get_and_update_games(weekNum)

    @classmethod
    def update_games(cls, weekNum):
        max_week = GameModel.get_max_week() or 0
        if int(weekNum) > max_week:
            return {'message': 'week not populated yet.'}

        return cls.get_and_update_games(weekNum)

    @classmethod
    def get_and_update_games(cls, weekNum):
        xml = urllib.request.urlopen(cls.nfl_endpoint.format(weekNum)).read()
        gamesXML = ET.fromstring(xml)

        for week in gamesXML:
            for game in week:
                game_id = game.get('gsis')
                gameModel = GameModel.find_by_game_id(game_id)

                if gameModel is None:
                    home_team_name = game.get('hnn')
                    home_team_city_abbr = game.get('h')
                    home_team_score = game.get('hs') or 0
                    away_team_name = game.get('vnn')
                    away_team_city_abbr = game.get('v')
                    away_team_score = game.get('vs') or 0
                    day_of_week = game.get('d')
                    time = game.get('t')
                    quarter = game.get('q')
                    weekNum = week.get('w')

                    date_string = game.get('eid')
                    yyyy_mm_dd = date_string[:
                                             4] + '-' + date_string[4:
                                                                    6] + '-' + date_string[6:
                                                                                           8]
                    game_date = datetime.strptime(yyyy_mm_dd, '%Y-%m-%d')

                    gameModel = GameModel(game_id, home_team_name,
                                          home_team_city_abbr, home_team_score,
                                          away_team_name, away_team_city_abbr,
                                          away_team_score, day_of_week, time,
                                          game_date, quarter, weekNum)
                    gameModel.upsert()
                else:
                    gameModel.home_team_score = game.get('hs') or 0
                    gameModel.away_team_score = game.get('vs') or 0
                    gameModel.day_of_week = game.get('d')
                    gameModel.time = game.get('t')
                    gameModel.quarter = game.get('q')
                    gameModel.weekNum = week.get('w')

                    date_string = game.get('eid')
                    yyyy_mm_dd = date_string[:
                                             4] + '-' + date_string[4:
                                                                    6] + '-' + date_string[6:
                                                                                           8]
                    gameModel.game_date = datetime.strptime(
                        yyyy_mm_dd, '%Y-%m-%d')
                    gameModel.upsert()
        return GameModel.get_games_by_week_json(weekNum)

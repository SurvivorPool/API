from models.game import GameModel
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib.request


class GameController():

    nfl_endpoint = 'http://www.nfl.com/ajax/scorestrip?season=2018&seasonType=PRE&week={}'

    @classmethod
    def update_games(cls, weekNum):
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
                    gameModel.home_team_name = game.get('hnn')
                    gameModel.home_team_city_abbr = game.get('h')
                    gameModel.home_team_score = game.get('hs') or 0
                    gameModel.away_team_name = game.get('vnn')
                    gameModel.away_team_city_abbr = game.get('v')
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
        return GameModel.get_games_by_week(weekNum)

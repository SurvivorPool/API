import requests
from models.nfl_team import NFLTeamModel

nfl_endpoint = 'https://feeds.nfl.com/feeds-rs/scores.json'


class NFLTeamController:

    @classmethod
    def populate_teams(cls):
        rss_feed = requests.get(nfl_endpoint)
        json_data = rss_feed.json()

        games = json_data['gameScores']

        for game in games:
            schedule_info = game['gameSchedule']
            home_team_info = schedule_info['homeTeam']
            away_team_info = schedule_info['visitorTeam']

            home_team_existence_check = NFLTeamModel.find_by_team_id(home_team_info['teamId'])
            away_team_existence_check = NFLTeamModel.find_by_team_id(away_team_info['teamId'])

            if home_team_existence_check is None:
                nfl_team = NFLTeamModel(home_team_info['teamId'], home_team_info['abbr'], home_team_info['cityState'],
                                        home_team_info['fullName'], home_team_info['nick'],
                                        home_team_info['conferenceAbbr'], home_team_info['divisionAbbr'])
                nfl_team.upsert()

            if away_team_existence_check is None:
                nfl_team = NFLTeamModel(away_team_info['teamId'], away_team_info['abbr'], away_team_info['cityState'],
                                        away_team_info['fullName'], away_team_info['nick'],
                                        away_team_info['conferenceAbbr'], away_team_info['divisionAbbr'])
                nfl_team.upsert()

        teams = NFLTeamModel.find_all_nfl_teams()

        return {'nfl_teams': [team.json() for team in teams]}


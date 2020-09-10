import requests
from models.nfl_team import NFLTeamModel

nfl_endpoint_old = 'https://feeds.nfl.com/feeds-rs/scores.json'

nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'


class NFLTeamController:

    @classmethod
    def populate_teams(cls):
        rss_feed = requests.get(nfl_endpoint)
        json_data = rss_feed.json()

        events = json_data['events']

        for event in events:
            competitions = event['competitions']
            teams = competitions[0]['competitors']

            home_team = next(filter(lambda team: team['homeAway'] == 'home', teams))
            away_team = next(filter(lambda team: team['homeAway'] == 'away', teams))

            home_team_existence_check = NFLTeamModel.find_by_team_id(home_team['id'])
            away_team_existence_check = NFLTeamModel.find_by_team_id(away_team['id'])

            if home_team_existence_check is None:
                home_info = home_team['team']
                nickname = ''
                if 'name' not in home_info:
                    nickname = home_info['displayName']
                else:
                    nickname = home_info['name']

                nfl_team = NFLTeamModel(home_team['id'], home_info['abbreviation'], home_info['location'],
                                        home_info['displayName'], nickname,
                                        "", "")
                nfl_team.upsert()

            if away_team_existence_check is None:
                away_info = away_team['team']
                if 'name' not in away_info:
                    nickname = away_info['displayName']
                else:
                    nickname = away_info['name']

                nfl_team = NFLTeamModel(away_team['id'], away_info['abbreviation'], away_info['location'],
                                        away_info['displayName'], nickname,
                                        "", "")
                nfl_team.upsert()

        teams = NFLTeamModel.find_all_nfl_teams()

        return {'nfl_teams': [team.json() for team in teams]}


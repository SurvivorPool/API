import requests
from models.stadium import StadiumModel


class StadiumController:
    nfl_endpoint = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'

    @classmethod
    def upsert_stadiums(cls):
        rss_feed = requests.get(cls.nfl_endpoint)

        json_data = rss_feed.json()

        events = json_data['events']

        for event in events:
            competitions = event['competitions']
            competition = competitions[0]

            stadium_info = competition['venue']
            stadium = StadiumModel.find_by_id(stadium_info['id'])

            if not stadium:
                new_stadium_id = stadium_info['id']
                new_stadium_city = stadium_info['address']['city']
                new_stadium_name = stadium_info['fullName']
                new_stadium_state = stadium_info["address"]["state"] if "state" in stadium_info["address"] else ""
                new_stadium_roof_type = "NA"
                new_stadium = StadiumModel(
                    new_stadium_id, new_stadium_city, new_stadium_name, new_stadium_state, new_stadium_roof_type)
                new_stadium.upsert()

    @classmethod
    def populate_stadiums(cls):
        cls.upsert_stadiums()

        stadiums = StadiumModel.find_all()
        return {'stadiums': [stadium.json() for stadium in stadiums]}

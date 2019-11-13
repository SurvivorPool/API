import requests
from models.stadium import StadiumModel


class StadiumController:
    nfl_endpoint = 'https://feeds.nfl.com/feeds-rs/scores.json'

    @classmethod
    def upsert_stadiums(cls):
        rss_feed = requests.get(cls.nfl_endpoint)

        json_data = rss_feed.json()

        games = json_data['gameScores']

        for game in games:
            schedule_info = game['gameSchedule']
            stadium_info = schedule_info['site']
            stadium = StadiumModel.find_by_id(stadium_info['siteId'])

            if not stadium:
                new_stadium_id = stadium_info['siteId']
                new_stadium_city = stadium_info['siteCity']
                new_stadium_name = stadium_info['siteFullname']
                new_stadium_state = stadium_info['siteState']
                new_stadium_roof_type = stadium_info['roofType']
                new_stadium = StadiumModel(new_stadium_id, new_stadium_city, new_stadium_name, new_stadium_state, new_stadium_roof_type) 
                new_stadium.upsert()


    @classmethod
    def populate_stadiums(cls): 
        cls.upsert_stadiums(cls)

        stadiums = StadiumModel.find_all()
        return {'stadiums': [stadium.json() for stadium in stadiums]}











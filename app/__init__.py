from flask import Flask, jsonify
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

# import firebase_admin
# from firebase_admin import credentials

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
# cred = credentials.Certificate('serviceAccountKey.json')
# default_app = firebase_admin.initialize_app(cred)


from app import routes
from resources.game import GamesList
from resources.user import User, UserExistence
from resources.playerTeams import PlayerTeam
from resources.league import League, LeaguesByUser, LeaguesList
from resources.pick import Pick

api.add_resource(GamesList, '/games/<string:weekNum>')
api.add_resource(User, '/user', '/user/<string:user_id>')
api.add_resource(UserExistence, '/user/exists/<string:user_id>')
api.add_resource(PlayerTeam, '/player_team', '/player_team/<string:team_id>')
api.add_resource(League, '/league', '/league/<string:league_id>')
api.add_resource(LeaguesList, '/leagues')
api.add_resource(LeaguesByUser, '/leagues/user/<string:user_id>')
api.add_resource(Pick, '/pick')
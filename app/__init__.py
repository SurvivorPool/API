from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from app import routes
from resources.game import Game, GamesList
from resources.user import User
from resources.playerTeams import PlayerTeam

api.add_resource(Game, '/game')
api.add_resource(GamesList, '/games/<string:weekNum>')
api.add_resource(User, '/user/<string:user_id>')
api.add_resource(PlayerTeam, '/player_team')
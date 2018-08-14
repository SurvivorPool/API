from flask import Flask, jsonify
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from app import routes
from resources.game import GamesList
from resources.user import User, UserExistence
from resources.playerTeam import PlayerTeam
from resources.league import League, LeaguesByUser, LeaguesList
from resources.pick import Pick
from resources.adminMessage import AdminMessage, AdminMessages

api.add_resource(GamesList, '/games/<string:weekNum>')
api.add_resource(User, '/user', '/user/<string:user_id>')
api.add_resource(UserExistence, '/user/exists/<string:user_id>')
api.add_resource(PlayerTeam, '/player_team', '/player_team/<string:team_id>')
api.add_resource(League, '/league', '/league/<string:league_id>')
api.add_resource(LeaguesList, '/leagues')
api.add_resource(LeaguesByUser, '/leagues/user/<string:user_id>')
api.add_resource(Pick, '/pick')
api.add_resource(AdminMessage, '/admin/message/<string:user_id>', '/admin/message')
api.add_resource(AdminMessages, '/admin/messages', methods=['GET'])
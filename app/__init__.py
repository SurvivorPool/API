from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
mail = Mail(app)
from models import *

from resources import GamesList, User, UserExistence, PlayerTeam,  League, LeaguesList, LeaguesByUser,\
    Pick, AdminMessage, AdminMessages, AdminGames, nflTeam

from app.email import send_email

api.add_resource(GamesList, '/games/<string:weekNum>')
api.add_resource(User, '/user', '/user/<string:user_id>')
api.add_resource(UserExistence, '/user/exists/<string:user_id>')
api.add_resource(PlayerTeam, '/player_team',
                 '/player_team/<string:team_id>')
api.add_resource(League, '/league', '/league/<string:league_id>')
api.add_resource(LeaguesList, '/leagues')
api.add_resource(LeaguesByUser, '/leagues/user/<string:user_id>')
api.add_resource(Pick, '/pick')
api.add_resource(AdminMessage, '/admin/message/<string:user_id>',
                 '/admin/message')
api.add_resource(AdminMessages, '/admin/messages', methods=['GET'])
api.add_resource(AdminGames, '/admin/games', methods=['PUT'])
api.add_resource(nflTeam, '/admin/nfl_teams/', methods=['PUT'])


@app.route('/email', methods=['GET'])
def email_request():
    send_email('test', app.config['MAIL_USERNAME'], ['alexmberardi@gmail.com'])

    return

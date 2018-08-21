from flask import Flask, jsonify
from flask_restplus import Resource, Api
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

import resources
from app.email import send_email
api.add_resource(resources.GamesList, '/games/<string:weekNum>')
api.add_resource(resources.User, '/user', '/user/<string:user_id>')
api.add_resource(resources.UserExistence, '/user/exists/<string:user_id>')
api.add_resource(resources.PlayerTeam, '/player_team',
                 '/player_team/<string:team_id>')
api.add_resource(resources.League, '/league', '/league/<string:league_id>')
api.add_resource(resources.LeaguesList, '/leagues')
api.add_resource(resources.LeaguesByUser, '/leagues/user/<string:user_id>')
api.add_resource(resources.Pick, '/pick')
api.add_resource(resources.AdminMessage, '/admin/message/<string:user_id>',
                 '/admin/message')
api.add_resource(resources.AdminMessages, '/admin/messages', methods=['GET'])
api.add_resource(resources.AdminGames, '/admin/games', methods=['PUT'])


#sender, recipients, text_body, html_body
@app.route('/email', methods=['GET'])
def email_request():
    send_email('test', app.config['MAIL_USERNAME'], ['alexmberardi@gmail.com'])

    return

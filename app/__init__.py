from flask import Flask, render_template
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
mail = Mail(app)
bootstrap = Bootstrap(app)

from resources import GamesList, User, UserExistence, PlayerTeam, PlayerTeamRegistrationStatus,  League, \
    LeaguesList, LeaguesByUser, Pick, AdminMessage, AdminMessages, AdminGames, NFLTeam, Stadium, AdvanceWeek,\
    AdminTeam, AdminTeams, UserMessage, AdminUserMessage, AdminUsers

from app.email import send_email

api.add_resource(GamesList, '/games/')
api.add_resource(User, '/user', '/user/<string:user_id>')
api.add_resource(UserExistence, '/user/exists/<string:user_id>')
api.add_resource(AdminUsers, '/admin/users/')
api.add_resource(PlayerTeam, '/player_team',
                 '/player_team/<string:team_id>')
api.add_resource(AdminTeams, '/admin/player_teams')
api.add_resource(League, '/league', '/league/<string:league_id>')
api.add_resource(LeaguesList, '/leagues')
api.add_resource(LeaguesByUser, '/leagues/user/<string:user_id>')
api.add_resource(Pick, '/pick')
api.add_resource(AdminMessage, '/admin/message/<string:user_id>',
                 '/admin/message')
api.add_resource(AdminMessages, '/admin/messages', methods=['GET'])
api.add_resource(AdminGames, '/admin/games', methods=['PUT'])
api.add_resource(NFLTeam, '/admin/nfl_teams', methods=['PUT'])
api.add_resource(Stadium, '/admin/stadiums')
api.add_resource(AdvanceWeek, '/admin/advance_week',  methods=['PUT'])
api.add_resource(AdminTeam, '/admin/player_team', methods=['PUT', 'DELETE'])
api.add_resource(UserMessage, '/user/<string:user_id>/messages')
api.add_resource(AdminUserMessage, '/admin/user/message')
api.add_resource(PlayerTeamRegistrationStatus, '/league/<string:league_id>/registration_status/<string:user_id>')

from models.user import UserModel

@app.route('/email', methods=['GET'])
def email_request():
    send_email('test', app.config['MAIL_USERNAME'], ['alexmberardi@gmail.com'])
    return render_template('league_lost.html', user=UserModel('user_id', 'alex berardi', 'alexmberardi@gmail.com', 'google.com'))



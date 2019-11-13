from flask import Flask, session
from flask_session import Session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from crowdsorting.app_resources.yamlReader import yamlReader

from flask_cas import CAS

app = Flask(__name__)

yamlReader.readConfig("config.yaml", app)

cas = CAS(app, '/cas')

app.secret_key = '398247b108570892173509827389057'
Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from crowdsorting.database.models import Project, Doc, Judge, Vote, Judgment
from crowdsorting.app_resources.sorting_algorithms.selection_algorithm import selection_algorithm
from crowdsorting.app_resources.sorting_algorithms.ACJProxy import ACJProxy

pairselector = ACJProxy()

from crowdsorting.app_resources.AdminModelView import *
from crowdsorting.app_resources import routes

admin = Admin(app, name='sorter', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(ProjectView(Project, db.session))
admin.add_view(DocView(Doc, db.session))
admin.add_view(JudgeView(Judge, db.session))
admin.add_view(VoteView(Vote, db.session))
admin.add_view(JudgmentView(Judgment, db.session))
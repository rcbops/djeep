import flask
from flaskext import sqlalchemy

app = flask.Flask(__name__)
app.config.from_object('rolemapper.config')

db = sqlalchemy.SQLAlchemy(app)

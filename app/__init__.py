from flask import Flask
from config import Config
from flask_mysqldb import MySQL
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = MySQL(app)
migrate = Migrate(app, db)

# this has to be after in-spite of pep8 cus app is being defined in line 4.
from app import routes


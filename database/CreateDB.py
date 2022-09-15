from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


class Database:
    def __init__(self, app, db_name='database', db_user='postgres', db_pass='postgres', db_host='127.0.0.1',
                 db_port='8081'):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_string = 'postgresql://{}:{}@{}:{}/{}'.format(self.db_user, self.db_pass, self.db_host, self.db_port,
                                                              self.db_name)
        self.app = app
        self.db = None
        self.login_manager = None

    def set_config(self):
        self.app.debug = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SECRET_KEY'] = 'loooong_secret_key'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.db_string

    def create_db(self):
        self.db = SQLAlchemy(self.app)
        return self.db

    def create_login_manager(self):
        self.login_manager = LoginManager(self.app)
        self.login_manager.login_view = 'login'
        return self.login_manager

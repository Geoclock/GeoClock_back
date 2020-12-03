from flask import Flask
from flask_migrate import Migrate

from Database import db
from Manager import manager
from templates import primary_routes, routes


app = Flask(__name__)
app.secret_key = 'hehehe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
manager.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()

import click
from flask_restful import Api
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import config
from base_model import IdModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def setup_db(app):
    db = SQLAlchemy(app, model_class=IdModel)
    Migrate(app, db)
    return db


def configure_cli(app, db):
    import pytest
    from models import User

    @app.cli.command("create-superuser")
    @click.argument("fname")
    @click.argument("lname")
    def create_user(fname, lname):
        user = User(fname=fname, lname=lname, _is_superuser=True)
        db.session.add(user)
        db.session.commit()

    @app.cli.command("test")
    def test():
        pytest.main(["-x", "tests", "-vv", "-W" "ignore::DeprecationWarning"])


def configure_api(app):
    from api_routes import routes
    api = Api(app, prefix=config.BASE_PATH, catch_all_404s=True, errors=config.ERRORS)

    for route in routes:
        api.add_resource(route[0], route[1])


app = create_app()
db = setup_db(app)
configure_cli(app, db)
configure_api(app)

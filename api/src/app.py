import click
from flask_restful import Api
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config
from base_model import IdModel

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app, model_class=IdModel)
migrate = Migrate(app, db)


# CLI Configuration
from models import User


@app.cli.command("create-superuser")
@click.argument("fname")
@click.argument("lname")
def create_user(fname, lname):
    user = User(fname=fname, lname=lname, _is_superuser=True)
    db.session.add(user)
    db.session.commit()


# API Definition
import resources
api = Api(app, prefix=config.BASE_PATH, catch_all_404s=True, errors=config.ERRORS)

api.add_resource(resources.BankListApi, "/bank/")
api.add_resource(resources.BankApi, "/bank/<int:bank_id>/")

api.add_resource(resources.BranchListApi, "/bank/<int:bank_id>/branch/")
api.add_resource(resources.BranchApi, "/bank/<int:bank_id>/branch/<branch_id>/")

api.add_resource(resources.StaffListApi, "/bank/<int:bank_id>/branch/<branch_id>/staff/")
api.add_resource(resources.StaffApi, "/bank/<int:bank_id>/branch/<branch_id>/staff/<int:staff_id>/")

api.add_resource(resources.AccountConfigListApi, "/bank/<int:bank_id>/account_config/")
api.add_resource(resources.AccountConfigApi, "/bank/<int:bank_id>/account_config/<int:account_config_id>/")

api.add_resource(resources.AccountListApi, "/bank/<int:bank_id>/account/")
api.add_resource(resources.AccountApi, "/bank/<int:bank_id>/account/<int:account_id>/")

api.add_resource(resources.TransactionListApi, "/bank/<int:bank_id>/account/<int:account_id>/transaction/")
api.add_resource(resources.TransactionApi, "/bank/<int:bank_id>/account/<int:account_id>/transaction/<int:transaction_id>/")

api.add_resource(resources.CheckListApi, "/bank/<int:bank_id>/account/<int:account_id>/check/")
api.add_resource(resources.CheckApi, "/bank/<int:bank_id>/account/<int:account_id>/check/<int:check_id>/")

api.add_resource(resources.UserListApi, "/user/")
api.add_resource(resources.UserApi, "/user/<int:user_id>/")

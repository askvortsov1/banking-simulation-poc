import os
import tempfile

import pytest
from alembic import command
from alembic.config import Config
from app import create_app, setup_db, configure_cli, configure_api


@pytest.fixture
def client():
    db_fd, path = tempfile.mkstemp()

    app = create_app()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(path)
    app.config['TESTING'] = True

    db = setup_db(app)
    configure_cli(app, db)
    configure_api(app)

    with app.test_client() as client:
        with app.app_context():
            config = Config("migrations/alembic.ini")
            config.set_main_option("script_location", "migrations")
            command.upgrade(config, "head")
        yield client

    os.close(db_fd)
    os.unlink(path)

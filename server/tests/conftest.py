import pytest

from server import create_app, db

#==================================
# Base fixtures to create a test app
#==================================

@pytest.fixture(scope='session')
def testapp():
    return create_app('server.config.TestingConfig') # set config to point to testing


@pytest.fixture()
def app(testapp):
    with testapp.app_context():
        db.create_all()
        yield testapp
        db.session.remove()
        db.drop_all()


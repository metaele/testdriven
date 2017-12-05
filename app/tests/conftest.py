import pytest

from app import create_app, db
from app.config import TestingConfig

#==================================
# Base fixture to create a test app
#==================================

@pytest.fixture(scope='session')
def testapp():
    return create_app(TestingConfig) # set config to point to testing


#===========================================
# The fixture http client to access test app
#===========================================
@pytest.fixture(scope='session')
def testapp_client(testapp):
    return testapp.test_client()


#===================================
# Database related fixtures
#===================================

@pytest.yield_fixture(scope='session')
def schemed_db(testapp):
    db.app = testapp
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture()
def tx_session(schemed_db):
    conn = schemed_db.engine.connect()
    tx = conn.begin()
    session = schemed_db.create_scoped_session(options={bind:conn, binds:{}})
    schemed_db.session = session
    yield session
    tx.rollback()
    conn.close()
    session.remove()

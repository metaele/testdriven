import pytest
from flask import current_app

from app import app

db_url = "postgres://postgres:postgres@users_db:5432/{}".format
cfg = "app.config.{}Config".format


def dev_app(config):
    app.config.from_object(config)
    return app


def test_app_is_development():
    app_tested = dev_app(cfg('Development'))
    assert app_tested.config['SECRET_KEY'] == 'my_secret'
    assert app_tested.config['DEBUG']
    assert current_app
    assert app_tested.config['SQLALCHEMY_DATABASE_URI'] == db_url('users_dev')


def test_app_is_testing():
    test_app = dev_app(cfg('Testing'))
    assert test_app.config['SECRET_KEY'] == 'my_secret'
    assert test_app.config['DEBUG']
    assert test_app.config['TESTING']
    assert not test_app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert test_app.config['SQLALCHEMY_DATABASE_URI'] == db_url('users_test')


def test_app_is_production():
    test_app = dev_app(cfg('Production'))
    assert test_app.config['SECRET_KEY'] == 'my_secret'
    assert not test_app.config['DEBUG']
    assert not test_app.config['TESTING']


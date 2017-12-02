import os
import datetime
import unittest

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)


@app.cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command()
def test():
    '''runs test - currently without coverage'''
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    tests_result = unittest.TextTestRunner(verbosity=2).run(tests)
    if tests_result.wasSuccessful():
        return 0
    return 1



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.datetime.utcnow()


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong'
    })

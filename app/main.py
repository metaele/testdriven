from . import create_app, db
from .api.models import User


app = create_app()


@app.cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command()
def seed_db():
    db.session.add(User('twicet', 'mrtwice@clearstride.io'))
    db.session.add(User('gofha', 'gofha@got.io'))
    db.session.commit()


@app.cli.command()
def test():
    '''runs test - currently without coverage'''
    import pytest
    pytest.main(['-s' , '-v', 'app/tests'])


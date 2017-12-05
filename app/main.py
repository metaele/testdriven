from . import create_app


app = create_app()


@app.cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command()
def test():
    '''runs test - currently without coverage'''
    import pytest
    pytest.main(['-v'])


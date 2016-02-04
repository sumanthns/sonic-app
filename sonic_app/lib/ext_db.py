from sqlalchemy import create_engine


def init_db():
    from sonic_app.app import config
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    db = engine.connect()
    return db

def rows_exist(rows):
    for row in rows:
        return True
    return False

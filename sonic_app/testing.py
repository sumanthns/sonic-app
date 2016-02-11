import unittest
from app import app
from ext import db


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_model(self, db_model, **kwargs):
        return db_model.query.filter_by(**kwargs).first()

    def create_model(self, db_model, **kwargs):
        _model_obj = db_model(**kwargs)
        db.session.add(_model_obj)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()

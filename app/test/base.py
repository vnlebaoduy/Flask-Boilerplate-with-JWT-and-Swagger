from flask_testing import TestCase

from app.main import db
from manage import app
from app.main.util.generator_sample_data import Seed


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        Seed.gen_role()
        Seed.gen_user()
        Seed.gen_permission()
        Seed.gen_user_role()
        Seed.gen_role_permission()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

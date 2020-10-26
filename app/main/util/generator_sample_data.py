from datetime import date, datetime
import logging
from app.main import db
from app.main.model.role import Role
from app.main.model.user import User
import uuid
import os
import json

os.chdir(os.path.dirname(__file__))


class Seed:
    @staticmethod
    def gen_role():
        logging.info("Generating Role ...")
        path = os.getcwd()
        with open(os.path.join(path, './sample/role.json')) as json_file:
            data = json.load(json_file)
            for p in data:
                user_role = Role(name=p['name'], description=p['description'], created_at=datetime.now(),
                                 created_by='')
                db.session.add(user_role)
            try:
                db.session.commit()
                logging.info("Generate Role Completed !")
            except:
                db.session.rollback()
                logging.error("Generate Role Failure !")

    @staticmethod
    def gen_user():
        logging.info("Generating User ...")
        path = os.getcwd()
        with open(os.path.join(path, './sample/user.json')) as json_file:
            data = json.load(json_file)
            for p in data:
                user_role = User(full_name=p['full_name'], email=p['email'], username=p['username'],
                                 password=p['password'], registered_on=datetime.utcnow(), public_id=str(uuid.uuid4()),
                                 is_active=True)
                db.session.add(user_role)
            try:
                db.session.commit()
                logging.info("Generate User Completed !")
            except:
                db.session.rollback()
                logging.error("Generate User Failure !")
